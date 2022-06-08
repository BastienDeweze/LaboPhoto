from order.models import Order

from django import forms

class CreateOrderForm(forms.ModelForm):
    
    """ Class configurant le formulaire de création de commande du site sur base d'un model de base de donnée.

    Returns:
        _type_: Le formulaire de création de commande.
    """

    class Meta:
        """ Configuration des métadonnées
                - model     : Le model sur lequel le formulaire doit agir.
                - fields    : Les champs que le formulaire doit prendre en compte.
        """
        model = Order
        fields = ['first_name', 'last_name', 'address', 'zipcode',  'city', 'country', 'email']

    def __init__(self, *args, **kwargs):
        
        """ Modification du style du formulaire
                - Ajout d'un placeholder
                - Ajout de la classe "form-control" (Bootstrap)
        """
        
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Prénom'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nom'
        self.fields['address'].widget.attrs['placeholder'] = 'Adresse'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['zipcode'].widget.attrs['placeholder'] = 'Code Postal'
        self.fields['city'].widget.attrs['placeholder'] = 'Ville'
        self.fields['country'].widget.attrs['placeholder'] = 'Pays'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'