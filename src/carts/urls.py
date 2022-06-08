from django.urls import path
from .views import cart, AddCart, CartList, RemoveCart, DeleteCartItem, AddOneCart
from django.contrib.auth.decorators import login_required

app_name = 'carts'

urlpatterns = [
    path('', CartList.as_view(), name="cart"),
    path('add_cart/<int:product_id>/', login_required(AddCart.as_view(), login_url='account:login'), name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', login_required(RemoveCart.as_view(), login_url='account:login'), name="remove_cart"),
    path('delete_cartitem/<int:product_id>/<int:cart_item_id>/', login_required(DeleteCartItem.as_view(), login_url='account:login'), name="delete_cartitem"),
    path('add_one_cartitem/<int:product_id>/<int:cart_item_id>/', login_required(AddOneCart.as_view(), login_url='account:login'), name="add_one_cartitem"),
]
