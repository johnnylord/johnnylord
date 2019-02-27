from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Post, Category

# Register your models here.
class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = { 'slug': ('name',) }


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('title',) }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)

