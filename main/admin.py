from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Hashtag


class CommentInline(admin.TabularInline):
    model = Comment
    # readonly_fields = ['likes', 'comment', 'user', 'created_at']


class PostAdmin(admin.ModelAdmin):
    fields = ('user', 'title', 'image')
    readonly_fields = ['created_at', 'likes']
    inlines = [CommentInline, ]


admin.site.register(Hashtag)
admin.site.register(Post, PostAdmin)

