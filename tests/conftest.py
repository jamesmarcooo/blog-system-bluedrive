# tests/conftest.py

import pytest
from typing import List, Callable
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from blog import PostStatus
from blog.models import Author, Post, Comment


# User and Author Factories

@pytest.fixture
def user_factory() -> Callable[..., User]:
    def create_user(username: str, is_staff: bool = False) -> User:
        return User.objects.create_user(username=username, password="password123", is_staff=is_staff)
    return create_user

@pytest.fixture
def author_factory(user_factory) -> Callable[..., Author]:
    def create_author(user: User = None, name: str = "Default Author") -> Author:
        if user is None:
            user = user_factory(username=name.replace(" ", "").lower())
        return Author.objects.create(name=name, email=f"{user.username}@test.com", user=user)
    return create_author


# Post Factory and Fixtures

@pytest.fixture
def post_factory(author_factory) -> Callable[..., Post]:
    def create_post(
        author: Author = None,
        title: str = "Default Title",
        content: str = "Default content.",
        status: str = PostStatus.PUBLISHED,
        active: bool = True,
    ) -> Post:
        if author is None:
            author = author_factory()
        return Post.objects.create(
            author=author, title=title, content=content, status=status, active=active
        )
    return create_post

@pytest.fixture
def multiple_posts(post_factory, author_factory) -> List[Post]:
    author1 = author_factory(name="Author One")
    author2 = author_factory(name="Author Two")

    return [
        # Active & Published Posts
        post_factory(author=author1, title="Active Post by Author One", active=True, status=PostStatus.PUBLISHED),
        post_factory(author=author2, title="Active Post by Author Two", active=True, status=PostStatus.PUBLISHED),
        # Inactive Post
        post_factory(author=author1, title="Inactive Post", active=False),
        # Draft Post
        post_factory(author=author2, title="Draft Post", status=PostStatus.DRAFT),
    ]


# API Client Fixtures

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def authenticated_author_client(api_client, author_factory) -> (APIClient, Author):
    author = author_factory(name="Test Author")
    api_client.force_authenticate(user=author.user)
    return api_client, author
