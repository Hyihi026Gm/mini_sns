from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("like/<int:post_id>/", views.like_toggle, name="like"),
]