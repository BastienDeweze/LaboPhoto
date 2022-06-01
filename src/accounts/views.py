from django.core.checks import messages
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from .forms import UserRegisterForm, AuthenticationFormCustom
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from .models import Account
from order.models import Order, State

# Create your views here.

class SignUpView(CreateView):

    """
    CreateView creant un compte et un profil d'utilisateur.
    """

    template_name = 'accounts/register.html'
    success_url = reverse_lazy('account:register')
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs) :
        if self.request.user.is_authenticated:
            return redirect('store:store')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) :
        form.instance.username = form.instance.email.split("@")[0]
        messages.success(self.request, "Votre compte a été créé avec succès.")
        return super().form_valid(form)

class Login(LoginView):

    """
    LoginView servant à loger un utilisateur
    """

    template_name="accounts/login.html"
    redirect_authenticated_user = True
    form_class = AuthenticationFormCustom

class Logout(LogoutView):
    pass

class Activate(RedirectView):

    permanent = False
    query_string = True
    pattern_name = reverse_lazy('carts:cart')

    def get_redirect_url(self, *args, **kwargs):


        return reverse('carts:cart')

class DetailAccount(DetailView) :
    template_name="accounts/myaccount.html"
    model = Account
    
    def get_object(self) :
        return print(self.request.user)
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["order_data"] = {}
        for state in State.objects.all() :
            context["order_data"][state.label] = state.order_set.filter(user_id=self.request.user).count()
        return context