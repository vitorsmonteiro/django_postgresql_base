from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("post_list", views.PostListView.as_view(), name="post_list"),
    path("post_create", views.PostCreateView.as_view(), name="post_create"),
    path("post_update/<int:pk>", views.PostUpdateView.as_view(), name="post_update"),
    path("post_detail/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("post_delete/<int:pk>", views.PostDeleteView.as_view(), name="post_delete"),
    path("topic_list", views.TopicListView.as_view(), name="topic_list"),
    path("topic_create", views.TopicCreateView.as_view(), name="topic_create"),
    path("topic_update/<int:pk>", views.TopicUpdateView.as_view(), name="topic_update"),
    path("topic_delete/<int:pk>", views.TopicDeleteView.as_view(), name="topic_delete"),
]
