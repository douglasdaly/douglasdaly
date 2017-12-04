
#
#   Imports
#
from django.contrib import admin

from .models import Post, Category


#
#   Admin Classes
#

class PostAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


#
#   Register Classes
#

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
