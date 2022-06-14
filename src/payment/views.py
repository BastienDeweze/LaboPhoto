from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from order.models import Order, OrderItems
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy, reverse
import stripe
from carts.models import Cart
from django.conf import settings
from .forms import CreateOrderForm

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class CartValidation(CreateView):
    
    """ Vue héritant de CreateView et servant à créer des nouvelles commandes en attente de payement.
    """
    
    model = Order
    template_name = "payment/checkout.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('payment:checkout_payment')
    
    def get_context_data(self, **kwargs) :
        
        """ Fonction hérité de la class CreateView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
        context = super().get_context_data(**kwargs)
        context["cartitems"] = Cart.objects.get(cart_id=self.request.user).cart_items()

        return context
    
    def form_valid(self, form) :
        
        """ Fonction hérité de la class CreateView et utilisé par la class CreateOrderForm qui est appelé lorsque le formulaire rempli par l'utilisateur est correct.
            Si aucune commande n'est déjà en attente, un commande en attente de payement est créé, sinon la commande abandonnée est modifié.

        Returns:
            Form: Le formulaire valide (remplissant toute les conditions de remplissage)
        """
        
        form.instance.total = Cart.objects.get(cart_id=self.request.user).total_price()
        if Order.objects.filter(user_id=self.request.user, is_valided=False).exists() :
            inst = Order.objects.filter(user_id=self.request.user, is_valided=False)
            fieldsName = [field.name for field in Order._meta.get_fields()]
            newData = {key: value for key, value in form.instance.__dict__.items() if value is not None and key in fieldsName}
            inst.update(**newData)
            return redirect(CartValidation.success_url)
        form.instance.user_id = self.request.user
        return super().form_valid(form)

class PayLandingPageView(TemplateView):
    
    """ Vue permettant à l'api stripe d'afficher sont formulaire de payement.
    """
    
    template_name = "payment/pay.html"

    def get_context_data(self, **kwargs):
        
        """ Fonction hérité de la class TemplateView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
        context = super(PayLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

def calculate_order_amount(user_cart):
    return user_cart.total_price()

class StripeView(View) :
    
    """ Vue appellée lorsqu'un utilisateur valide le formulaire de payement
    """
    
    def post(self, request, *args, **kwargs) :
        
        """ Fonction appellée lorsqu'un utilisateur valide le formulaire de payement.
            Retourne des données au format Json car celles-ci doivent etre lisible en JavaScript.
        """
    
    
        try:
            # data = json.loads(request.data)
            # Create a PaymentIntent with the order amount and currency
            user_cart = Cart.objects.get(cart_id=self.request.user)
            order = Order.objects.get(user_id=self.request.user, is_valided=False)
            intent = stripe.PaymentIntent.create(
                amount = calculate_order_amount(user_cart),
                currency='eur',
                payment_method_types=["card", "sepa_debit"],
                metadata = {"order_id": order.pk},
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})

class SuccessPayment(RedirectView):
    
    """ Vue servant remplir la commande en attente de payement avec le panier de l'utilisateur en cas de succes du payement.
        Suite à ce, la commande n'est plus en attende de payement et est validé.
        Cette class hérite de la class RedirectView car directement après l'action de cette vue, une redirection doit etre effectué. Cette vue ne sert pas à afficher des données à l'utilisateur.
    """
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle rempli la commande avec les données se trouvant dans le panier, update les stock et passe la commande au status validée.
        """
        
        order = Order.objects.get(user_id=self.request.user, is_valided=False)
        card = Cart.objects.get(cart_id=self.request.user)
        for cart_item in card.cart_items() :
            OrderItems.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            cart_item.product.update_stock(cart_item.quantity)
        card.cart_items().delete()
        order.is_valided = True
        order.save()
        return reverse('carts:cart')