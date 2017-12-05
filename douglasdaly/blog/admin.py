
#
#   Imports
#
from django.contrib import admin

from .models import Post, Category, Tag, PostToTag


#
#   Admin Classes
#

class PostToTagInline(admin.TabularInline):
    model = PostToTag
    extra = 1


class PostAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostToTagInline]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


#
#   Register Classes
#

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
