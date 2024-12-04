from django.shortcuts import render, redirect
from .models import Streak


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    # Get Latest Streak
    streak = Streak.objects.filter(has_ended=False)
    if streak:
        streak = streak[0]
        streak_color = "orange"

    return render(
        request,
        "streaks/home.html",
        context={
            "streak": streak,
            "streak_color": streak_color,
        },
    )
