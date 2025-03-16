from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("post_list", views.PostList.as_view(), name="post_list"),
    path("post_create", views.PostCreate.as_view(), name="post_create"),
    path("post_update/<int:pk>", views.PostUpdate.as_view(), name="post_update"),
    path("post_detail/<int:pk>", views.PostDetail.as_view(), name="post_detail"),
    path("post_delete/<int:pk>", views.PostDelete.as_view(), name="post_delete"),
    path("topic_list", views.TopicList.as_view(), name="topic_list"),
    path("topic_create", views.TopicCreate.as_view(), name="topic_create"),
    path("topic_update/<int:pk>", views.TopicUpdate.as_view(), name="topic_update"),
    path("topic_delete/<int:pk>", views.TopicDelete.as_view(), name="topic_delete"),
]
