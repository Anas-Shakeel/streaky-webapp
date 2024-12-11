from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.utils import timezone
from .models import Streak


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    date_today = timezone.localtime(timezone.now()).date()

    # Get Streak, or Create one
    try:
        streak = Streak.objects.get(user=request.user)
    except Streak.DoesNotExist:
        if Streak.objects.all().count() == 0:
            return Http404()

        # Create a default one
        streak = Streak(user=request.user, date_started=date_today)
        streak.save()

    # Streak State
    if streak.date_updated:
        # How many days since Last Increase
        days_since_last_update = (date_today - streak.date_updated).days

        if days_since_last_update == 1:
            # Ready to increase
            streak.already_increased = False
            streak.save()

        elif days_since_last_update > 1:
            # Break Streak
            streak.break_streak()
        else:
            # Cannot increase today
            pass

    # Streak color
    if streak.already_increased:
        streak_color = "grey"
    elif streak.count <= 50:
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


def reset_streak(request):
    if request.user.is_authenticated:
        streak = get_object_or_404(Streak, user=request.user)
        streak.reset()

    return redirect("streaks:home")


def account(request):
    return render(request, "streaks/account.html")
