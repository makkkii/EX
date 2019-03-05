from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Board, Post, Topic, UserProfile

class BoardAdmin(ModelAdmin):
  list_display = [
    '__str__', 'get_posts_count', 'created_at'
  ]
  search_fields = [
    'name', 'description'
  ]
  readonly_fields = ['created_at']


class PostAdmin(ModelAdmin):
  list_display = [
    '__str__', 'created_by', 'created_at'
  ]
  search_fields = [
    'message', 'topic'
  ]
  readonly_fields = ['created_at']

class TopicAdmin(ModelAdmin):
  list_display = [
    '__str__', 'board', 'starter', 'views'
  ]
  search_fields = [
    'subject', 'board'
  ]
  readonly_fields = ['created_at']


admin.site.register(Board, BoardAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
