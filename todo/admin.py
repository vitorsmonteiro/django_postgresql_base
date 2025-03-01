from django.contrib import admin

from todo.models import Task, TaskCategory, TaskStatus

admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(TaskStatus)
