import pytest

from django.urls import reverse
from rest_framework import status

from blog.models import Comment, Post

pytestmark = pytest.mark.django_db

class TestPostListingAndFiltering:
    def test_post_list_queryset_only_returns_active_posts(self, api_client, multiple_posts):
        url = reverse("post-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        expected_count = Post.objects.filter(active=True).count()
        assert len(response.data) == expected_count

        for post_data in response.data:
            assert post_data["active"] is True


class TestPostRetrieval:
    def test_retrieve_single_post_includes_comments(self, api_client, post_factory):
        post = post_factory()
        Comment.objects.create(post=post, content="First comment.")
        Comment.objects.create(post=post, content="Second comment.")

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert "comments" in response_data
        assert len(response_data["comments"]) == 2
        assert response_data["comments"][0]["content"] == "First comment."


class TestPostCreation:
    def test_create_post_as_authenticated_author_succeeds(self, authenticated_author_client):
        client, author = authenticated_author_client
        url = reverse("post-list")
        data = {"title": "A Brand New Post", "content": "Here is some new content."}

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert response.data["title"] == data["title"]
        assert response.data["author_name"] == author.name
        assert Post.objects.filter(title=data["title"]).exists()

    def test_create_post_as_unauthenticated_user_fails(self, api_client):
        url = reverse("post-list")
        data = {"title": "Unauthorized Post", "content": "This should not be created."}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.count() == 0

    def test_create_post_by_user_without_author_profile_fails(self, api_client, user_factory):
        regular_user = user_factory(username="regularuser")
        api_client.force_authenticate(user=regular_user)

        url = reverse("post-list")
        data = {"title": "Post by non-author", "content": "This should fail."}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You do not have an author profile" in response.data["detail"]
        assert Post.objects.count() == 0

    def test_create_post_with_duplicate_title_fails(self, authenticated_author_client, post_factory):
        client, author = authenticated_author_client

        post_factory(title="A Unique Title")
        url = reverse("post-list")

        data = {"title": "A Unique Title", "content": "Some other content."}
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "A post with this title already exists." in str(response.data['title'])
        assert Post.objects.count() == 1


class TestPostEditing:
    def test_edit_post_as_owner_succeeds(self, authenticated_author_client, post_factory):
        client, author = authenticated_author_client
        post = post_factory(author=author, title="Original Title")
        url = reverse("post-detail", kwargs={"pk": post.pk})
        data = {"title": "Updated Title", "active": False}

        response = client.patch(url, data, format="json")
        post.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert post.title == "Updated Title"
        assert post.active is False

    def test_edit_post_as_different_author_fails(self, api_client, author_factory, post_factory):
        owner_author = author_factory(name="Owner Author")
        post = post_factory(author=owner_author)

        imposter_author = author_factory(name="Imposter Author")
        api_client.force_authenticate(user=imposter_author.user)

        url = reverse("post-detail", kwargs={"pk": post.pk})
        data = {"title": "Illegal Update"}

        response = api_client.patch(url, data, format="json")
        post.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert post.title != "Illegal Update"


class TestPostDeletion:
    def test_delete_post_as_owner_succeeds(self, authenticated_author_client, post_factory):
        client, author = authenticated_author_client
        post = post_factory(author=author)
        url = reverse("post-detail", kwargs={"pk": post.pk})

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(pk=post.pk).exists()

    def test_delete_post_as_different_author_fails(self, api_client, author_factory, post_factory):
        owner_author = author_factory(name="Owner Author")
        post = post_factory(author=owner_author)

        imposter_author = author_factory(name="Imposter Author")
        api_client.force_authenticate(user=imposter_author.user)

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.filter(pk=post.pk).exists()


class TestCommentCreation:
    def test_create_comment_as_logged_in_user_succeeds(self, api_client, user_factory, post_factory):
        post = post_factory(active=True)
        user = user_factory(username="commenter")
        api_client.force_authenticate(user=user)
        url = reverse("post-comment-create", kwargs={"post_pk": post.pk})
        data = {"content": "This is a great comment!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"] == user.username
        assert post.comments.count() == 1

    def test_create_comment_as_anonymous_user_succeeds(self, api_client, post_factory):
        post = post_factory(active=True)
        url = reverse("post-comment-create", kwargs={"post_pk": post.pk})
        data = {"content": "An anonymous thought."}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"] is None
        assert post.comments.count() == 1

    def test_create_comment_on_inactive_post_fails(self, api_client, post_factory):
        post = post_factory(active=False)
        url = reverse("post-comment-create", kwargs={"post_pk": post.pk})
        data = {"content": "Trying to comment on an inactive post."}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert post.comments.count() == 0

    def test_create_comment_on_nonexistent_post_fails(self, authenticated_author_client):
        client, _ = authenticated_author_client

        non_existent_post_id = 999
        url = reverse("post-comment-create", kwargs={"post_pk": non_existent_post_id})
        data = {"content": "A comment for a ghost post."}

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Post not found" in response.data["error"]
