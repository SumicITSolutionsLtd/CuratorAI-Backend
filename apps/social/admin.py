from django.contrib import admin
from .models import Post, PostImage, PostLike, PostSave, Comment, CommentLike

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostLike)
admin.site.register(PostSave)
admin.site.register(Comment)
admin.site.register(CommentLike)

