from django.db import models
from accounts.models import Account
from store.models import Product


# Create your models here.

class State (models.Model):
    
    label           = models.CharField(max_length=10)


class Order (models.Model):
    
    user_id         = models.ForeignKey(Account, null=True, on_delete = models.SET_NULL)
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    email           = models.EmailField(max_length=100)
    address         = models.CharField(max_length=100)
    zipcode         = models.CharField(max_length=6)
    city            = models.CharField(max_length=50)
    country         = models.CharField(max_length=50)
    total           = models.FloatField()
    state_id        = models.ForeignKey(State, default=3, null=True, on_delete = models.SET_NULL)
    is_valided      = models.BooleanField(default=False)
    date            = models.DateTimeField(auto_now=True)
    
    @property
    def euro_price(self) :
        return self.total / 100


class OrderItems(models.Model) :
    
    product         = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order           = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    quantity        = models.IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name
    

