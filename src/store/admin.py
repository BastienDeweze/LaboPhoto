from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    
    """Ajout de la gestion des pellicule dans l'espace administrateur
    
    Args:
        admin.ModelAdmin (UserAdmin): Class hérité permettant de modifier l'espace administrateur du site 
        par rapport a un model de base de donnée
    """

    list_display = ('product_name', 'price', 'stock', 'created_on', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name', )}
    # exclude = ('product_name', 'slug',)

admin.site.register(Product, ProductAdmin)