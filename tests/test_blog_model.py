import pytest
from django.db import IntegrityError
from django.contrib.auth.models import User
from blog.models import Author, Post, Comment
from datetime import datetime
from blog import PostStatus

pytestmark = pytest.mark.django_db


class TestAuthorModel:
    def test_author_creation(self, author_factory):
        author = author_factory(name="James Marco")
        assert isinstance(author, Author)
        assert author.name == "James Marco"
        assert author.email == "jamesmarco@test.com"
        assert Author.objects.count() == 1

    def test_author_string_representation(self, author_factory):
        author = author_factory(name="Test Name")
        assert str(author) == "Test Name"

    def test_deleting_user_sets_author_user_to_null(self, author_factory, user_factory):
        user = user_factory(username="testuser_to_delete")
        author = author_factory(user=user)
        assert author.user == user

        user.delete()
        author.refresh_from_db()

        assert author.user is None


class TestPostModel:
    def test_post_creation_defaults(self, post_factory):
        post = post_factory(title="My First Post")
        assert post.status == PostStatus.PUBLISHED
        assert post.active is True
        assert isinstance(post.published_date, datetime)
        assert Post.objects.count() == 1

    def test_post_string_representation(self, post_factory):
        post = post_factory(title="A Very Interesting Title")
        assert str(post) == "A Very Interesting Title"

    def test_deleting_author_cascades_to_posts(self, author_factory, post_factory):
        author = author_factory()
        post_factory(author=author)
        post_factory(author=author)
        assert Post.objects.count() == 2

        author.delete()

        assert Post.objects.count() == 0


class TestCommentModel:
    def test_comment_creation(self, post_factory):
        post = post_factory()
        comment = Comment.objects.create(post=post, content="This is a test comment.")
        assert isinstance(comment.created, datetime)
        assert Comment.objects.count() == 1
        assert post.comments.count() == 1

    def test_comment_string_representation_with_user(self, post_factory, user_factory):
        user = user_factory(username="commenter")
        post = post_factory(title="A Post")
        comment = Comment.objects.create(post=post, user=user, content="My thoughts.")
        assert str(comment) == "Comment by commenter on A Post"

    def test_comment_string_representation_anonymous(self, post_factory):
        post = post_factory(title="Another Post")
        comment = Comment.objects.create(post=post, content="Anonymous feedback.")
        assert str(comment) == "Comment by Anonymous on Another Post"

    def test_deleting_post_cascades_to_comments(self, post_factory):
        post = post_factory()
        Comment.objects.create(post=post, content="Comment 1")
        Comment.objects.create(post=post, content="Comment 2")
        assert Comment.objects.count() == 2

        post.delete()

        assert Comment.objects.count() == 0

    def test_deleting_user_sets_comment_user_to_null(self, post_factory, user_factory):
        user = user_factory(username="user_to_be_deleted")
        post = post_factory()
        comment = Comment.objects.create(post=post, user=user, content="A comment.")
        assert comment.user == user

        user.delete()
        comment.refresh_from_db()

        assert comment.user is None
