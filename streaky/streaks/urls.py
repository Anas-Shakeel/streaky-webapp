from django.urls import path
from . import views


app_name = "streaks"
urlpatterns = [
    path("", views.home, name="home"),
    path("edit/", views.edit_streak, name="edit"),
    path("increase/", views.increase_streak, name="increase"),
    path("reset/", views.reset_streak, name="reset"),
    path("account/", views.account, name="account"),
]
