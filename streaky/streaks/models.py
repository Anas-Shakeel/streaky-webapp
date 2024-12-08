from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Streak title...")
    description = models.TextField(default="Streak short description...")
    count = models.IntegerField(default=0)
    date_started = models.DateTimeField(default=timezone.now)
    date_updated = models.DateField(blank=True, null=True)
    already_increased = models.BooleanField(default=False)

    def break_streak(self):
        """Breaks the current streak"""
        self.already_increased = False
        self.date_started = timezone.localtime(timezone.now())
        self.date_updated = None
        self.count = 0
        self.save()

    def reset(self):
        """Resets the streaks as new."""
        self.title = "Streak title..."
        self.description = "Streak short description..."
        self.count = 0
        self.date_started = None
        self.date_updated = None
        self.already_increased = False
        self.save()

    def __str__(self) -> str:
        return "%s - %s" % (self.user.username, self.title)
