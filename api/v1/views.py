from typing import Type

import django_filters

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters.rest_framework import (
    DateFromToRangeFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework import (
    exceptions,
    generics,
    permissions,
    serializers,
    status,
    viewsets,
)
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.v1.serializers import (
    CommentSerializer,
    PostCreateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from blog.models import Author, Comment, Post


class PostFilter(FilterSet):
    published_date = DateFromToRangeFilter()
    author_name = django_filters.CharFilter(
        field_name="author__name",
        lookup_expr="icontains",
    )
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["title", "author_name", "published_date"]


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self) -> QuerySet[Post]:
        queryset: QuerySet = Post.objects.all()
        if self.action == "list":
            return queryset.filter(active=True).select_related("author")
        if self.action == "retrieve":
            return queryset.select_related("author").prefetch_related("comments")
        return queryset

    def get_serializer_class(
        self,
    ) -> Type[PostListSerializer | PostDetailSerializer | PostCreateSerializer]:
        if self.action == "list":
            return PostListSerializer
        if self.action == "create":
            return PostCreateSerializer
        return PostDetailSerializer

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        if not self.request.user.is_authenticated:
            raise exceptions.PermissionDenied("You must be logged in to create a post.")

        try:
            author: Author = Author.objects.get(user=self.request.user)
            serializer.save(author=author)
        except Author.DoesNotExist as err:
            raise exceptions.PermissionDenied(
                "You do not have an author profile to create a post.",
            ) from err


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Response, **_kwargs: dict) -> Response:
        post_id: int = self.kwargs.get("post_pk")
        try:
            post: Post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not post.active:
            return Response(
                {"error": "Cannot comment on an inactive post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = request.user if request.user.is_authenticated else None
        serializer.save(post=post, user=user)

        headers: dict[str, str] = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
