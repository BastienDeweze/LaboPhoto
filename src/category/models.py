from django.db import models
from django.urls import reverse

# Create your models here.

class ColorCategory(models.Model):
    
    """ Model de base de donnée représentant une couleur de pellicule.
    """
    
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    size = models.IntegerField(default=0)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories/", blank=True)

    class Meta:
        verbose_name = 'color category'
        verbose_name_plural = 'color categories'

    def get_url(self):
        
        """ Fonction renvoyant la vue correspondant à la catégorie.

        Returns:
            _type_: Le chemin vers la vu correspondant à cette catégorie.
        """
        return reverse('store:product_by_category', kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs) :
        
        """ Héritage de la fonction "save()" qui est appelé lors d'un update de record.
            Lorsqu'une catégorie est modifier, il faut recalculer les nom de chaque produit lié à cette catégorie.
        """
        
        for product in self.product_set.all() :
            product.save()
        return super().save(*args, **kwargs)

class SizeCategory(models.Model):
    
    """ Model de base de donnée représentant une couleur de pellicule.
    """
    
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    size = models.IntegerField(default=0)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories/", blank=True)

    class Meta:
        verbose_name = 'size category'
        verbose_name_plural = 'size categories'

    def get_url(self):
        
        """ Fonction renvoyant la vue correspondant à la catégorie.

        Returns:
            _type_: Le chemin vers la vu correspondant à cette catégorie.
        """
        
        return reverse('store:product_by_category', kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs) :
        
        """ Héritage de la fonction "save()" qui est appelé lors d'un update de record.
            Lorsqu'une catégorie est modifier, il faut recalculer les nom de chaque produit lié à cette catégorie.
        """
        
        for product in self.product_set.all() :
            product.save()
        return super().save(*args, **kwargs)