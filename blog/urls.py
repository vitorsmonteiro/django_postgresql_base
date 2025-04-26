from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("post_list", views.BlogPostListView.as_view(), name="post_list"),
    path("post_create", views.BlogPostCreateView.as_view(), name="post_create"),
    path(
        "post_update/<int:pk>", views.BlogPostUpdateView.as_view(), name="post_update"
    ),
    path(
        "post_detail/<int:pk>", views.BlogPostDetailView.as_view(), name="post_detail"
    ),
    path(
        "post_delete/<int:pk>", views.BlogPostDeleteView.as_view(), name="post_delete"
    ),
    path("topic_list", views.TopicListView.as_view(), name="topic_list"),
    path("topic_create", views.TopicCreateView.as_view(), name="topic_create"),
    path("topic_update/<int:pk>", views.TopicUpdateView.as_view(), name="topic_update"),
    path("topic_delete/<int:pk>", views.TopicDeleteView.as_view(), name="topic_delete"),
]
