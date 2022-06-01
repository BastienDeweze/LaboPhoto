from django.shortcuts import render
from django.views.generic.base import RedirectView
from store.models import Product
from .models import Cart, CartItem
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class RemoveCart(RedirectView):

    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):

        cart = Cart.objects.get(cart_id=self.request.user)
        cart_items = cart.cart_items()

        try:
            cart_item = cart_items.get(id=kwargs['cart_item_id'])
            cart_item.quantity -= 1
            cart_item.save()
            if cart_item.quantity <= 0:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        return reverse('carts:cart')

class AddCart(RemoveCart):


    def get_redirect_url(self, *args, **kwargs):

        product = Product.objects.get(pk=kwargs['product_id'])
        cart = Cart.objects.get(cart_id=self.request.user)
        cart_items = cart.cart_items()
        print(f"cart_items = {cart_items}")
        if cart_items.filter(product=product).exists() :
            item = cart_items.get(product=product)
            item.quantity += 1
            item.save()
        else :
            CartItem.objects.create(product=product, cart=cart, quantity=1)


        return reverse('carts:cart')


class AddOneCart(RemoveCart):

    def get_redirect_url(self, *args, **kwargs):

        cart = Cart.objects.get(cart_id=self.request.user)
        cart_items = cart.cart_items()

        try:
            cart_item = cart_items.get(id=kwargs['cart_item_id'])
            cart_item.quantity += 1
            cart_item.save()
            
        except CartItem.DoesNotExist:
            pass

        return reverse('carts:cart')

class DeleteCartItem(AddCart):

    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):

        cart = Cart.objects.get(cart_id=self.request.user)
        cart_items = cart.cart_items()

        try:
            cart_item = cart_items.get(id=kwargs['cart_item_id'])
            cart_item.delete()
        except:
            pass

        return reverse('carts:cart')


def cart(request):
    return render(request, 'store/cart.html')

class CartList(ListView):

    model = CartItem
    context_object_name = "cartitems"
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs) :
        try:
            context =  super().get_context_data(**kwargs)
            cart = Cart.objects.get(cart_id=self.request.user)
            cartitem = cart.cart_items()

            context['total_price'] = sum([c.quantity * c.product.price for c in cartitem])
            context['total_quantity'] = cartitem.aggregate(Sum('quantity'))['quantity__sum']
            context['tva'] = sum([c.quantity * c.product.tva_product() for c in cartitem])
            context['grand_total'] = context['total_price'] + context['tva']

        except ObjectDoesNotExist:
            pass #just ignore

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        cart = Cart.objects.get(cart_id=self.request.user)
        queryset = queryset.filter(cart=cart, is_active=True)

        return  queryset