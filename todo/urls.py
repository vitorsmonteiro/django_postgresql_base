from django.urls import path

from todo import views

app_name = "todo"

urlpatterns = [
    path("", views.home, name="todo"),
    path("todo_create", views.create_todo, name="todo_create"),
]
