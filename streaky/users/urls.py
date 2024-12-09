from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("signup/", views.signup_user, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    path("change_username/", views.change_username, name="change_username"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
]
