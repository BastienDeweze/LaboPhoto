from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    
    """ Class configurant le formulaire d'inscription sur le site en héritant du formulaire de base proposé par Django.

    Returns:
        _type_: Le formulaire d'inscription sur le site.
    """


    class Meta:
        """ Configuration des métadonnées
                - model     : Le model sur lequel le formulaire doit agir.
                - fields    : Les champs que le formulaire doit prendre en compte.
        """
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        
        """ Modification du style du formulaire
                - Ajout d'un placeholder
                - Ajout de la classe "form-control" (Bootstrap)
        """
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationFormCustom(AuthenticationForm):
    
    """Class configurant le formulaire de connexion au site en héritant du formulaire de base proposé par Django.

    Returns:
        _type_: Le formulaire de connexion au site.
    """
    
    def __init__(self, *args, **kwargs):
        
        """ Modification du style du formulaire
                - Ajout d'un placeholder
                - Ajout de la classe "form-control" (Bootstrap)
        """
        
        super(AuthenticationFormCustom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'