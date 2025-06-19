from blog import PostStatus

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts", db_index=True)
    status = models.CharField(max_length=10, choices=PostStatus.CHOICES, default=PostStatus.DRAFT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
