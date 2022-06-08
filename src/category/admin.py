from django.contrib import admin
from .models import ColorCategory, SizeCategory

# Register your models here.

class ColorCategoryAdmin(admin.ModelAdmin):
    
    """Ajout de la gestion des couleurs de pellicule dans l'espace administrateur
    
    Args:
        admin.ModelAdmin (UserAdmin): Class hérité permettant de modifier l'espace administrateur du site 
        par rapport a un model de base de donnée
    """
    
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class SizeCategoryAdmin(admin.ModelAdmin):
    
    """Ajout de la gestion des tailles de pellicule dans l'espace administrateur
    
    Args:
        admin.ModelAdmin (UserAdmin): Class hérité permettant de modifier l'espace administrateur du site 
        par rapport a un model de base de donnée
    """
    
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(ColorCategory,ColorCategoryAdmin)

admin.site.register(SizeCategory,SizeCategoryAdmin)