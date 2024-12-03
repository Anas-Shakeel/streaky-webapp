from django.contrib import admin
from .models import Streak


# Register your models here.
class StreakAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "count", "date_added", "date_ended", "has_ended")


admin.site.register(Streak, StreakAdmin)
