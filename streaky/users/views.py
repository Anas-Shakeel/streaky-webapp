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
        # Get the fields
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Validate the fields
        message = ""
        if not username:
            message = "Invalid username! try again."
        elif User.objects.filter(username=username).first():
            message = "Username already exists! try another."
        elif len(username) < 4:
            message = "Username must contain atleast 4 characters!"
        elif len(username) > 30:
            message = "Username can only contain 30 characters at most!"
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
                    message = f"Illegal character {char} in username. Avoid these {ILLEGAL_CHARS} characters."
                    return render(request, "users/signup.html", {"message": message})

            # Create the User
            user = User(username=username, password=make_password(password))
            user.save()

            # Login
            login(request, user)
            return redirect("streaks:home")

        return render(request, "users/signup.html", {"message": message})

    # Logged in?
    if request.user.is_authenticated:
        return redirect("streaks:home")

    # If user is not logged and not posted, render the page normally!
    return render(request, "users/signup.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("users:login")


def change_username(request):
    if request.method == "POST":
        username = request.POST["username"]
        message = ""

        # Validate the username
        if not username:
            message = "Invalid username! try again."
        elif User.objects.filter(username=username).first():
            message = "Username already exists! try another."
        elif len(username) > 30:
            message = "Username can only contain 30 characters at most!"
        elif len(username) < 4:
            message = "Username must contain atleast 4 characters!"
        else:
            # Finally check for illegal characters
            for char in ILLEGAL_CHARS:
                if char in username:
                    message = f"Illegal character {char} in username. Avoid these {ILLEGAL_CHARS} characters."
                    return render(request, "streaks/account.html", {"message": message})

            # Everything is ok at this point. change the username now!
            user = User.objects.get(username=request.user.username)
            user.username = username
            user.save()

            return redirect("streaks:account")

        # something went wrong! redirect to account page and pass the message
        return render(request, "streaks/account.html", {"message": message})

    return redirect("streaks:account")


def change_password(request):
    if request.method == "POST":
        # Get the fields
        old_pass = request.POST.get("old_password", "")
        new_pass = request.POST.get("new_password", "")
        confirm_pass = request.POST.get("confirm_password", "")

        # Get the current user
        current_user = User.objects.get(username=request.user.username)

        # Validate the fields
        message = ""
        if not old_pass:
            message = "Old password field must not be empty"
        elif not new_pass:
            message = "New password field must not be empty"
        elif not confirm_pass:
            message = "Confirm password field must not be empty"
        elif new_pass != confirm_pass:
            message = "New password does not match confirm password"
        elif new_pass == old_pass:
            message = "New password must not be same as old password"
        elif len(new_pass) > 30:
            message = "Password can only contain 30 characters at most"
        elif len(new_pass) < 4:
            message = "Password must contain atleast 4 characters"
        elif not check_password(old_pass, current_user.password):
            message = "Incorrect old password, try again!"
        else:
            # All well, proceed
            current_user.password = make_password(new_pass)
            current_user.save()

            # Login the user
            login(request, current_user)

            return redirect("streaks:account")

        # something went wrong, re-render with error
        return render(request, "streaks/account.html", {"message": message})

    return redirect("streaks:account")


def delete_account(request):
    # request POST and User logged in?
    if request.method == "POST" and request.user.is_authenticated:
        # Get the password
        password = request.POST.get("password", "")

        # Get user account
        user = User.objects.get(username=request.user.username)

        message = ""

        # Don't delete admin account
        if user.is_superuser:
            message = "Cannot delete admin account from here"
        elif not check_password(password, user.password):
            message = "Incorrect Password, please (don't) try again"
        else:
            # Delete the account at this point
            user.delete()
            return redirect("streaks:home")

        return render(request, "streaks/account.html", {"message": message})

    return redirect("streaks:home")
