from django.urls import path
from .views import ListAccountOrder, ChangeState
from django.contrib.auth.decorators import login_required

app_name = 'order'

urlpatterns = [
    path('orders/', login_required(ListAccountOrder.as_view(), login_url='account:login'), name="orders"),
    path('change-state/<int:state_id>/<int:order_id>', login_required(ChangeState.as_view(), login_url='account:login'), name="change_state"),
]