from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from api.v1.views import CommentCreateAPIView, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
        path(
        "posts/<int:post_pk>/comments/",
        CommentCreateAPIView.as_view(),
        name="post-comment-create",
    ),

    # Documentation - Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
