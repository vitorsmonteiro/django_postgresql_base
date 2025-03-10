from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("topic_list", views.TopicList.as_view(), name="topic_list"),
    path("topic_create", views.TopicCreate.as_view(), name="topic_create"),
    path("topic_update/<int:pk>", views.TopicUpdate.as_view(), name="topic_update"),
    path("topic_delete/<int:pk>", views.TopicDelete.as_view(), name="topic_delete"),
]
