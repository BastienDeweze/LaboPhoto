from django.urls import path
from .views import CartValidation, StripeView, PayLandingPageView, SuccessPayment
from django.contrib.auth.decorators import login_required

app_name = 'payment'

urlpatterns = [
    path('validate-data/', login_required(CartValidation.as_view(), login_url='account:login'), name="checkout_cart"),
    path('create-payment-intent/', login_required(StripeView.as_view(), login_url='account:login'), name="create_payment"),
    path('checkout/', login_required(PayLandingPageView.as_view(), login_url='account:login'), name="checkout_payment"),
    path('success/', login_required(SuccessPayment.as_view(), login_url='account:login'), name="success"),
]
