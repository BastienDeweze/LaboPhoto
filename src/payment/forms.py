from order.models import Order

from django import forms

class CreateOrderForm(forms.ModelForm):
    

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'zipcode',  'city', 'country', 'email']

    def __init__(self, *args, **kwargs):
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