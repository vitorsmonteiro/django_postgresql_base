from django.urls import path

from common import views

app_name = "common"

urlpatterns = [
    path("", views.home, name="home"),
]
