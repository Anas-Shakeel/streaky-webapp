from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Streak


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # Get Streak
    streak = get_object_or_404(Streak, user=request.user)

    # Streak color
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


def increase_streak(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    if request.method == "POST":
        streak = get_object_or_404(Streak, user=request.user)

        # Increase if not already.
        if not streak.already_increased:
            streak.count += 1
            streak.date_updated = timezone.localtime(timezone.now()).date()
            streak.already_increased = True
            streak.save()

            # Send status 200 as json response
            return JsonResponse({"count": streak.count})

        return JsonResponse({"count": streak.count})

    # For GET requests
    return redirect("streaks:home")


def edit_streak(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # Get User's streak
    streak = get_object_or_404(Streak, user=request.user)

    # Submitted Edit?
    if request.method == "POST":
        streak_title = request.POST.get("title", "")
        streak_description = request.POST.get("description", "")

        # Update streak
        streak.title = streak_title
        streak.description = streak_description
        streak.save()

        return redirect("streaks:home")

    return render(
        request,
        "streaks/edit.html",
        context={"streak": streak},
    )
