from django.contrib import admin

from blog.models import BlogPost, Comment, Topic

admin.site.register(Topic)
admin.site.register(BlogPost)
admin.site.register(Comment)
