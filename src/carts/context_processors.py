from .models import Cart, CartItem
from django.db.models import Sum

def counter(request):
    total_quantity = 0
    if 'admin' in request.path:
        return {}

    else :
        try :
            cart = Cart.objects.get(cart_id=request.user)
            cartitem = CartItem.objects.filter(cart=cart, is_active=True)
            total_quantity = cartitem.aggregate(Sum('quantity'))['quantity__sum']
            total_quantity = total_quantity if total_quantity is not None else 0

        except :
            total_quantity = 0

    return dict(total_item=total_quantity) 