from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    count = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    already_increased = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "%s - %s" % (self.user.username, self.title)
