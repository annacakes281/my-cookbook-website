from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Tip


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # can view and search posts in the admin view

    list_display = ('recipe_name', 'slug', 'status', 'posted_on')
    search_fields = ['recipe_name', 'ingredients']
    prepopulated_fields = {'slug': ('recipe_name', )}
    list_filter = ('status', 'posted_on')
    summernote_fields = ('excerpt', 'ingredients', 'recipe_steps',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # can view and search comments in the admin view

    list_display = ('name', 'comment', 'post', 'posted_on')
    search_fields = ('name', 'email', 'comment')
    list_filter = ('name', 'posted_on')


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    # can view and search tips in the admin view

    list_display = ('name', 'tip', 'post', 'posted_on')
    search_fields = ('name', 'email', 'tip',)
    list_filter = ('name', 'posted_on')
