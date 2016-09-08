from django.contrib import admin

from graph import models as graph_models


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created_time', 'message']
    list_filter = ['user']


admin.site.register(graph_models.Post, PostAdmin)
