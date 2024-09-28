from django.contrib import admin
from .models import Post, Comment, Interactions

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug', 'owner', 'publish', 'status']
    list_filter = ['status', 'created_at', 'publish', 'owner']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['owner']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'post', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['comment']
    ordering = ['created_at']

admin.site.register(Interactions)