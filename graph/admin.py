from daterange_filter.filter import DateRangeFilter
from django.contrib import admin

from graph import models as graph_models


class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ['post__user__username', 'post__user__email', 'title', 'url']
    list_display = ['id', 'title', 'type', 'url']
    list_filter = ['post__user', 'type']


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['post__user__username', 'post__user__email', 'message', 'from_json']
    list_display = ['id', 'created_time', 'message']
    list_filter = ['post__user', ('created_time', DateRangeFilter)]


class PostAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email', 'message', 'story']
    list_display = ['id', 'user', 'created_time', 'message']
    list_filter = ['user', ('created_time', DateRangeFilter)]


admin.site.register(graph_models.Attachment, AttachmentAdmin)
admin.site.register(graph_models.Comment, CommentAdmin)
admin.site.register(graph_models.Post, PostAdmin)
