from django.db import models
from store.models import Product
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    
    """ Model de base de donnée représentant le panier d'un utilisateur.
        Un panier est créé à la création d'un compte et est unique à ce compte.
    """
    cart_id         = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_added      = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_id)
    
    def cart_items(self) :
        
        """ Fonction réalisant la relation inverse vers les ligne d'article se trouvant dans le panier de l'utilisateur.
        Nouveau commentaire

        Returns:
            QuerySet: L'ensemble des articles se trouvant dans le panier de l'utilisateur.
        """
        return self.cartitem_set.all()
    
    def total_price(self) :
        
        """ Fonction retournant le prix total que l'utilisateur devra payer (TVA comprise) si il veux acheer l'ensemble du panier.

        Returns:
            int: Le prix total en cent.
        """
        
        total = 0
        for item in self.cart_items() :
            total += item.sub_total_tva()
        return int(total * 100)


class CartItem(models.Model):
    
    """ Model de base de donnée represnant les lignes contenu dans un panier.
    """
    
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)

    def sub_total(self):
        
        """ Fonction renvoyant le total d'une ligne en fonction du nombre d'article souhaité.

        Returns:
            float: Prix de la ligne.
        """
        
        return self.product.price * self.quantity
    
    def sub_total_tva(self):
        
        """ Fonction renvoyant le total d'une ligne en fonction du nombre d'article souhaité TVA comprise.

        Returns:
            float: Prix de la ligne TVA comprise.
        """
        
        return self.sub_total() + (self.product.tva_product() * self.quantity)

    def __str__(self):
        return self.product.product_name
