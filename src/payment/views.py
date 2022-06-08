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
    
    model = Order
    template_name = "payment/checkout.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('payment:checkout_payment')
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["cartitems"] = Cart.objects.get(cart_id=self.request.user).cart_items()

        return context
    
    def form_valid(self, form) :
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
    template_name = "payment/pay.html"

    def get_context_data(self, **kwargs):
        context = super(PayLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

def calculate_order_amount(user_cart):
    return user_cart.total_price()

class StripeView(View) :
    
    def post(self, request, *args, **kwargs) :
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
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):
        order = Order.objects.get(user_id=self.request.user, is_valided=False)
        card = Cart.objects.get(cart_id=self.request.user)
        for cart_item in card.cart_items() :
            OrderItems.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            cart_item.product.uodate_stock(cart_item.quantity)
        card.cart_items().delete()
        order.is_valided = True
        order.save()
        return reverse('carts:cart')