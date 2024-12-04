from django.contrib import admin

from todo.models import Task, TaskCategory, TaskStatus

admin.register(Task)
admin.register(TaskCategory)
admin.register(TaskStatus)
