from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main_project.api import api_v1
from main_project.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, TESTING

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", api_v1.urls),
    path("", include("common.urls")),
    path("", include("authentication.urls")),
    path("todo/", include("todo.urls")),
    path("blog/", include("blog.urls")),
]

if DEBUG:
    urlpatterns = [*urlpatterns, *static(MEDIA_URL, document_root=MEDIA_ROOT)]

if not TESTING:
    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
