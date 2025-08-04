from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "slug", "count_like"]


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["body", "id", "count_like", "user"]


admin.site.register(Comment, CommentAdmin)
