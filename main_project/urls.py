from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls")),
    path("", include("authentication.urls")),
    path("todo/", include("todo.urls")),
]

if not settings.TESTING:
    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
