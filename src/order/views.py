from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy, reverse
from .models import Order, State
from datetime import datetime

# Create your views here.

class ListAccountOrder(ListView) :
    
    """ Vue h-héritant de la class ListView et servant à lister les commandes d'un utilisateur
    """
    
    template_name="accounts/account_order.html"
    context_object_name = "orderslst"
    model = Order
    
    def get_context_data(self, **kwargs) :
        
        """ Fonction hérité de la class ListView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
        context = super().get_context_data(**kwargs)
        context["states"] = State.objects.all()
        return context
    
    def get_queryset(self):
        
        """ Fonction hérité de la class ListView et servant à renvoyer les commandes d'un utilisateur en tenant compte des filtres appliqué par l'utilisateur.

        Returns:
            QuerySet: La liste des articles à afficher dans le shop.
        """
        
        queryset = super().get_queryset().filter(is_valided=True)
        
        if self.request.GET.get('order_id') :
            queryset = queryset.filter(pk=self.request.GET.get('order_id'))
        
        if self.request.GET.get('client_id') :
            queryset = queryset.filter(user_id__id=self.request.GET.get('client_id'))
        
        if self.request.GET.get('date') :
            date_time_obj = datetime.strptime(self.request.GET.get('date'), '%m/%d/%Y')
            queryset = queryset.filter(date__gt=date_time_obj)
        
        if self.request.GET.get('date_to') :
            date_time_obj = datetime.strptime(self.request.GET.get('date_to'), '%m/%d/%Y')
            queryset = queryset.filter(date__lt=date_time_obj)
        
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
    
    """ Vue servant à changer l'état d'une commande.
        Cette class hérite de la class RedirectView car directement après l'action de cette vue, une redirection doit etre effectué. Cette vue ne sert pas à afficher des données à l'utilisateur.
    """
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy('order:orders')

    def get_redirect_url(self, state_id, order_id, *args, **kwargs):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            Elle recupere le nouvel état de la commande choisi par l'admin et l'associe à la commande souhaité.
        """
        
        if self.request.user.is_admin :
            order = Order.objects.get(pk=order_id)
            state = State.objects.get(pk=state_id)
            order.state_id = state
            order.save()
        return reverse('order:orders')