from django.db import models
from category.models import ColorCategory, SizeCategory
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True, blank=True)
    slug            = models.SlugField(max_length=200, unique=True, blank=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.FloatField()
    images          = models.ImageField(upload_to='photos/products', default='photos/products/defaultproduct.jpg')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    color_category  = models.ForeignKey(ColorCategory, on_delete=models.CASCADE, null=True, default=None)
    size_category   = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, null=True, default=None)
    created_on      = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    tva             = models.FloatField(default=21.0)
    
    def save(self, *args, **kwargs) :
        self.product_name = f"{self.size_category.category_name} - {self.color_category.category_name}"
        print(self.product_name)
        self.slug = slugify(self.product_name)
        return super(Product, self).save(*args, **kwargs)
    
    def uodate_stock(self, quantity) :
        if self.stock > quantity :
            self.stock -= quantity
        else :
            self.stock = 0
        self.save()

    def tva_product(self):
        return self.price * self.tva / 100

    def __str__(self):
        return self.product_name