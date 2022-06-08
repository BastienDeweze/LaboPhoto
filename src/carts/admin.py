from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    
    """Ajout de la gestion des paniers des utilisateurs dans l'espace administrateur
    
    Args:
        admin.ModelAdmin (UserAdmin): Class hérité permettant de modifier l'espace administrateur du site 
        par rapport a un model de base de donnée
    """

    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    
    """Ajout de la gestion des lignes de paniers des utilisateurs dans l'espace administrateur
    
    Args:
        admin.ModelAdmin (UserAdmin): Class hérité permettant de modifier l'espace administrateur du site 
        par rapport a un model de base de donnée
    """

    list_display = ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)