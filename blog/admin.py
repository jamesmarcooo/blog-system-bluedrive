from django.contrib import admin

from blog.models import Author, Comment, Post

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
