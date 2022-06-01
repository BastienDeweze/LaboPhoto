from django.urls import path
from .views import CartValidation, StripeView, PayLandingPageView, SuccessPayment

app_name = 'payment'

urlpatterns = [
    path('validate-data/', CartValidation.as_view(), name="checkout_cart"),
    path('create-payment-intent/', StripeView.as_view(), name="create_payment"),
    path('checkout/', PayLandingPageView.as_view(), name="checkout_payment"),
    path('success/', SuccessPayment.as_view(), name="success"),
]
