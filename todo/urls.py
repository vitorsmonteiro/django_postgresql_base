from django.urls import path

from todo import views

app_name = "todo"

urlpatterns = [
    path("", views.home, name="home"),
    path("todo_create", views.create_todo, name="todo_create"),
]
