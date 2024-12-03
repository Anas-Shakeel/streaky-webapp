from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password


# These characters should not be in the usernames
ILLEGAL_CHARS = """ \\/:;*?"'`|%/,"""


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Illegal characters in username?
        for char in ILLEGAL_CHARS:
            if char in username:
                message = f"Illegal character {char} in username. Avoid these {ILLEGAL_CHARS} characters."
                return render(request, "users/login.html", {"message": message})

        # Authenticate
        user = authenticate(request, username=username, password=password)

        # Authenticated?
        if user:
            login(request, user)
            return redirect("streaks:home")
        else:
            return render(
                request,
                "users/login.html",
                {"message": "Invalid Credentials, try again!"},
            )

    # Already logged in?
    if request.user.is_authenticated:
        return redirect("streaks:home")

    return render(request, "users/login.html")


def signup_user(request):
    if request.method == "POST":
        # Get the username, email, password and confirm password
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Validate the fields
        message = ""
        # Validations
        if not username:
            message = "Invalid username! try again."
        elif User.objects.filter(username=username).first():
            message = "Username already exists! try another."
        elif len(username) < 4:
            message = "Username must contain atleast 4 characters!"
        elif len(username) > 30:
            message = "Username can only contain 30 characters at most!"
        elif not email:
            message = "Invalid email! try again."
        elif User.objects.filter(email=email).first():
            message = "Email already exists! try another."
        elif password != confirm_password:
            message = "Password must be same as confirm password"
        elif len(password) < 4:
            message = "Password must have atleast 4 characters"
        elif len(password) > 30:
            message = "Password can only contain 30 characters at most!"
        else:
            # Finally check for illegal characters
            for char in ILLEGAL_CHARS:
                if char in username:
                    message = f"Illegal character '{
                        char}' not allowed. Avoid these ({ILLEGAL_CHARS})"
                    return render(request, "users/signup.html", {"message": message})

            # Everything is ok at this point, now signup
            user = User(
                username=username, email=email, password=make_password(password)
            )
            user.save()
            login(request, user)
            return redirect("index")

        # if anything above, goes down, this will execute...
        return render(request, "users/signup.html", {"message": message})

    # Logged in?
    if request.user.is_authenticated:
        return redirect("streaks:home")

    # If user is not logged and not posted, render the page normally!
    return render(request, "users/signup.html")
