from rest_framework import serializers
from blog.models import Author, Post, Comment
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "email"]

