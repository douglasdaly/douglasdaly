
#
#   Imports
#
from django.contrib import admin

from .models import Post, Category, Tag, BlogSettings, CustomJS


#
#   Admin Classes
#

class PostAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'posted', 'published')
    list_filter = ('published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


#
#   Register Classes
#

admin.site.register(BlogSettings)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CustomJS)
