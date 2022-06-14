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
    
    """ Vue servant à décrémenté de 1 le nombre d'article, pour un seul article.
        Cette class hérite de la class RedirectView car directement après l'action de cette vue, une redirection doit etre effectué. Cette vue ne sert pas à afficher des données à l'utilisateur.
    """

    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle décrémente de 1 l'article choisi par l'utilisateur dans son panier.
            Si le nombre d'article est à zéro, cet article est supprimé du panier.
        """

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
    
    """ Vue servant à incrémenter de 1 le nombre d'article, pour un seul article.
        Cette class hérite de la class RemoveCart car elle sert juste à incrémenter à la place de décrémenter.
    """


    def get_redirect_url(self, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle incrémente de 1 l'article choisi par l'utilisateur dans son panier.
            Si l'article n'est pas présent dans le panier, il est ajouté à celui-ci.
        """

        product = Product.objects.get(pk=kwargs['product_id'])
        cart = Cart.objects.get(cart_id=self.request.user)
        cart_items = cart.cart_items()
        if cart_items.filter(product=product).exists() :
            item = cart_items.get(product=product)
            item.quantity += 1
            item.save()
        else :
            CartItem.objects.create(product=product, cart=cart, quantity=1)


        return reverse('carts:cart')


class AddOneCart(RemoveCart):
    
    """ Vue servant à incrémenter de 1 le nombre d'article, pour un seul article.
        Cette class hérite de la class RemoveCart car elle sert juste à incrémenter à la place de décrémenter.
    """

    def get_redirect_url(self, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle incrémente de 1 l'article choisi par l'utilisateur dans son panier.
            Si l'article n'est pas présent dans le panier, il est ajouté à celui-ci.
        """

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
    
    """ Vue servant à incrémenter de 1 le nombre d'article, pour un seul article.
        Cette class hérite de la class AddCart car elle sert juste à incrémenter à la place de décrémenter.
    """

    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle permt de supprimer un article du panier de l'utilisateur connecté avant de le rediriger vers son panier.
        """

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
    
    """ Vue servant à lister l'ensemble des lignes du panier d'un utilisateur.
    """

    model = CartItem
    context_object_name = "cartitems"
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs) :
        
        """ Fonction hérité de la class ListView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
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
        
        """ Fonction hérité de la class ListView et servant à renvoyer le panier de l'utilisateur.

        Returns:
            QuerySet: Les articles dans le panier de l'utilisateur connecté.
        """
        
        queryset = super().get_queryset()
        cart = Cart.objects.get(cart_id=self.request.user)
        queryset = queryset.filter(cart=cart, is_active=True)

        return  queryset