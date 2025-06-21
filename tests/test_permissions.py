from unittest.mock import MagicMock

import pytest

from api.permissions import IsAuthorOrReadOnly

pytestmark = pytest.mark.django_db


class TestIsAuthorOrReadOnly:

    def test_safe_methods_are_always_allowed(self, user_factory, post_factory):
        permission = IsAuthorOrReadOnly()

        get_request = MagicMock()
        get_request.method = "GET"

        head_request = MagicMock()
        head_request.method = "HEAD"

        options_request = MagicMock()
        options_request.method = "OPTIONS"

        post_obj = post_factory()

        assert permission.has_object_permission(get_request, MagicMock(), post_obj) is True
        assert permission.has_object_permission(head_request, MagicMock(), post_obj) is True
        assert permission.has_object_permission(options_request, MagicMock(), post_obj) is True

    def test_unsafe_method_allowed_for_object_owner(self, author_factory, post_factory):
        permission = IsAuthorOrReadOnly()

        author = author_factory()
        post_obj = post_factory(author=author)

        request = MagicMock()
        request.method = "PUT"
        request.user = author.user

        assert permission.has_object_permission(request, MagicMock(), post_obj) is True

    def test_unsafe_method_denied_for_different_user(self, author_factory, user_factory, post_factory):
        permission = IsAuthorOrReadOnly()

        owner_author = author_factory(name="Owner")
        post_obj = post_factory(author=owner_author)

        imposter_user = user_factory(username="imposter")

        request = MagicMock()
        request.method = "DELETE"
        request.user = imposter_user

        assert permission.has_object_permission(request, MagicMock(), post_obj) is False

    def test_unsafe_method_denied_for_anonymous_user(self, author_factory, post_factory):
        permission = IsAuthorOrReadOnly()
        post_obj = post_factory()

        anonymous_user = MagicMock()
        anonymous_user.is_authenticated = False

        request = MagicMock()
        request.method = "PATCH"
        request.user = anonymous_user


        assert permission.has_object_permission(request, MagicMock(), post_obj) is False
