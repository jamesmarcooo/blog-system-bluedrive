import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response

from blog.models import Post, Comment
from api.serializers import PostListSerializer, PostDetailSerializer, CommentSerializer


class PostFilter(FilterSet):
    published_date = DateFromToRangeFilter()
    author_name = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["title", "author_name", "published_date"]


class PostViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        if self.action == "list":
            return Post.objects.filter(active=True).select_related("author")
        return Post.objects.all().select_related("author")

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=user)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
