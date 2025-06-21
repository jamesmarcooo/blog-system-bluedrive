from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from blog.models import Post


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, _view: View, obj: Post) -> bool:
        # NOTE: Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(obj.author.user == request.user)
