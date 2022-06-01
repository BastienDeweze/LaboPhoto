from django.urls import path
from .views import cart, AddCart, CartList, RemoveCart, DeleteCartItem, AddOneCart
from django.contrib.auth.decorators import login_required

app_name = 'carts'

urlpatterns = [
    path('', CartList.as_view(), name="cart"),
    path('add_cart/<int:product_id>/', login_required(AddCart.as_view(), login_url='account:login'), name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', RemoveCart.as_view(), name="remove_cart"),
    path('delete_cartitem/<int:product_id>/<int:cart_item_id>/', DeleteCartItem.as_view(), name="delete_cartitem"),
    path('add_one_cartitem/<int:product_id>/<int:cart_item_id>/', AddOneCart.as_view(), name="add_one_cartitem"),
]
