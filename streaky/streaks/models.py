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
    date_ended = models.DateTimeField(blank=True, null=True)

    def has_ended(self) -> bool:
        return bool(self.date_ended)

    def __str__(self) -> str:
        return "%s - %s" % (self.user.username, self.title)
