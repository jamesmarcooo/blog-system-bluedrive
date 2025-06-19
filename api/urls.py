from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet, CommentCreateAPIView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:post_pk>/comments/", CommentCreateAPIView.as_view(), name="post-comment-create"),
]
