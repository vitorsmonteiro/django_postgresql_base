from django.urls import path

from authentication import views

app_name = "authentication"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_user", views.create_user, name="create_user"),
    path("edit_user", views.edit_user, name="edit_user"),
    path("reset_password", views.reset_password, name="reset_password"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("generate_token", views.generate_token, name="generate_token"),
]
