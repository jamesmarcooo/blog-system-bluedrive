from rest_framework import serializers

from blog.models import Author, Comment, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "email"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "user", "created"]

    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Comment must be at least 2 characters long.")
        if len(value) > 3000:
            raise serializers.ValidationError("Comment cannot exceed 3000 characters.")
        return value


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "published_date", "author_name", "active"]


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published_date",
            "author_name",
            "active",
            "status",
            "comments",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content","published_date", "author_name","status"]


    def validate_title(self, value):
        if Post.objects.filter(title__exact=value).exists():
            raise serializers.ValidationError("A post with this title already exists.")
        return value
