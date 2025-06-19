import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter
from rest_framework import viewsets

from blog.models import Post
from api.serializers import PostListSerializer


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
