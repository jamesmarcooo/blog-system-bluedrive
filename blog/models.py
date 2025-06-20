from django.contrib.auth.models import User
from django.db import models

from blog import PostStatus


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
        db_index=True,
    )
    status = models.CharField(
        max_length=10,
        choices=PostStatus.CHOICES,
        default=PostStatus.DRAFT,
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        user_display = self.user.username if self.user else "Anonymous"
        return (
            f"Comment by {user_display} "
            f"on {self.post.title}"
        )
