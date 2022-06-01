from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id         = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_added      = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_id)
    
    def cart_items(self) :
        return self.cartitem_set.all()
    
    def total_price(self) :
        total = 0
        for item in self.cart_items() :
            total += item.sub_total_tva()
        return int(total * 100)


class CartItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def sub_total_tva(self):
        return self.sub_total() + (self.product.tva_product() * self.quantity)

    def __str__(self):
        return self.product.product_name