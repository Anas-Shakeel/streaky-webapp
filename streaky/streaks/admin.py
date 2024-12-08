from django.contrib import admin
from .models import Streak


# Register your models here.
class StreakAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "count", "date_started")


admin.site.register(Streak, StreakAdmin)
