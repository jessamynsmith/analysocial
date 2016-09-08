from daterange_filter.filter import DateRangeFilter
from django.contrib import admin

from graph import models as graph_models


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_time', 'message']
    list_filter = ['user', ('created_time', DateRangeFilter)]


admin.site.register(graph_models.Post, PostAdmin)
