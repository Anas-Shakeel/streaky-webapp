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
        fillcolor = "orange"

    return render(
        request,
        "streaks/home.html",
        {"streak": streak, "fillcolor": fillcolor},
    )
