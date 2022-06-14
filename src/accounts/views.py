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
from order.models import State
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

class SignUpView(CreateView):

    """
    CreateView creant un compte et un profil d'utilisateur.
    """

    template_name = 'accounts/register.html'
    success_url = reverse_lazy('account:register')
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs) :
        
        """ Fonction hérité de CreateView et étant appelé avant toute action de la vue.
            Si l'utilisateur veut acceder à la vu alors qu'il est déjà authentifié, il sera redirigé vers le store.
        """
        
        if self.request.user.is_authenticated:
            return redirect('store:store')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) :
        
        """ Fonction hérité de la class CreateView et utilisé par la class UserRegisterForm qui est appelé lorsque le formulaire rempli par l'utilisateur est correct.
            Le username de l'utilisateur correspond à la partie de l'email avant le "@". Le username n'est pas un champs unique. c'est l'email qui l'est.

        Returns:
            Form: Le formulaire valide (remplissant toute les conditions de remplissage)
        """
        
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
    
    """ Class héritant de LogoutView et étant appelé lorsqu'un utilisateur souhaite se lougout du site.
    """
    
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        
        """ Fonction hérité de LogoutView et étant appelé avant toute action de la vue.
            La fonction supprime les cookies venant de l'api stripe afin d'eviter les clash d'utilisateurs.
        """
        response = super().dispatch(request, *args, **kwargs)
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response

class DetailAccount(DetailView) :
    
    """ Vue servant à afficher les données d'un utilisateur en particulié dans le detail.
    """
    
    template_name="accounts/myaccount.html"
    model = Account
    
    def get_object(self) :
        
        """ Fonction hérité DetailView et servant à recupérer l'oject de type Record devant est mit dans le context du template.

        Returns:
            Record: Le record venant de la base de donnée et devant etre donné au template
        """
        
        return print(self.request.user)
    
    def get_context_data(self, **kwargs) :
        
        """ Fonction hérité de la class DetailView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
        context = super().get_context_data(**kwargs)
        context["order_data"] = {}
        for state in State.objects.all() :
            context["order_data"][state.label] = state.order_set.filter(user_id=self.request.user, is_valided=True).count()
        return context