from django.contrib import admin
from .models import ColorCategory, SizeCategory

# Register your models here.

class ColorCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class SizeCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(ColorCategory,ColorCategoryAdmin)

admin.site.register(SizeCategory,SizeCategoryAdmin)