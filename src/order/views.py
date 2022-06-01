from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy, reverse
from .models import Order, State

# Create your views here.

class ListAccountOrder(ListView) :
    template_name="accounts/account_order.html"
    context_object_name = "orderslst"
    model = Order
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["states"] = State.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.GET.get('order_id') :
            queryset = queryset.filter(pk=self.request.GET.get('order_id'))
        
        if self.request.GET.get('client_id') :
            queryset = queryset.filter(user_id__id=self.request.GET.get('client_id'))
        
        if self.request.GET.get('date') :
            split_date = self.request.GET.get('date').split("/")
            queryset = queryset.filter(date__year=split_date[2], date__month=split_date[0], date__day=split_date[1])
        
        if self.request.GET.get('state_id') :
            queryset = queryset.filter(state_id__id=int(self.request.GET.get('state_id')))
        
        if self.request.GET.get('min_price') and self.request.GET.get('min_price') != "0" :
            queryset = queryset.filter(total__gte=int(self.request.GET.get('min_price')) * 100 )
        
        if self.request.GET.get('max_price') and self.request.GET.get('max_price') != "2000" :
            queryset = queryset.filter(total__lte=int(self.request.GET.get('max_price')) * 100 )
            
        if not self.request.user.is_admin: 
            return queryset.filter(user_id = self.request.user)
        
        return queryset

class ChangeState(RedirectView):
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy('order:orders')

    def get_redirect_url(self, state_id, order_id, *args, **kwargs):
        order = Order.objects.get(pk=order_id)
        state = State.objects.get(pk=state_id)
        order.state_id = state
        order.save()
        return reverse('order:orders')