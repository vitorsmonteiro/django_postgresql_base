from django.urls import path

from todo.views import todo

app_name = "todo"

urlpatterns = [
    path("", todo, name="todo"),
]
