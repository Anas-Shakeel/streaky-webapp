from django.shortcuts import render, redirect, get_object_or_404
from .models import Streak


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # Get Latest Streak
    streak = get_object_or_404(Streak, user=request.user)

    # Decide color
    if streak.count <= 50:
        streak_color = "#40AFFF"
    elif streak.count <= 100:
        streak_color = "#40FF90"
    elif streak.count <= 365:
        streak_color = "#FFA640"
    else:
        streak_color = "#BF66FF"

    return render(
        request,
        "streaks/home.html",
        context={
            "streak": streak,
            "streak_color": streak_color,
        },
    )


def edit_streak(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # Get User's streak
    streak = get_object_or_404(Streak, user=request.user)

    # Submitted Edit?
    if request.method == "POST":
        return redirect("streaks:home")

    return render(
        request,
        "streaks/edit.html",
        context={"streak": streak},
    )
