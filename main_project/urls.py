from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from main_project.api import api_v1, api_v2

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api_v1.urls),
    path("api/v2/", api_v2.urls),
    path("", include("common.urls")),
    path("", include("authentication.urls")),
    path("todo/", include("todo.urls")),
]

if not settings.TESTING:
    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
