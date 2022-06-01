from django.db import models
from django.urls import reverse

# Create your models here.


# class Category(models.Model):

#     category_name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     description = models.TextField(max_length=255, blank=True)
#     cat_image = models.ImageField(upload_to="photos/categories/", blank=True)

#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'

#     def get_url(self):
#         return reverse('store:product_by_category', kwargs={"category_slug": self.slug})

#     def __str__(self):
#         return self.category_name

class ColorCategory(models.Model):
    
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    size = models.IntegerField(default=0)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories/", blank=True)

    class Meta:
        verbose_name = 'color category'
        verbose_name_plural = 'color categories'

    def get_url(self):
        return reverse('store:product_by_category', kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs) :
        for product in self.product_set.all() :
            product.save()
        return super().save(*args, **kwargs)

class SizeCategory(models.Model):
    
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    size = models.IntegerField(default=0)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories/", blank=True)

    class Meta:
        verbose_name = 'size category'
        verbose_name_plural = 'size categories'

    def get_url(self):
        return reverse('store:product_by_category', kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs) :
        for product in self.product_set.all() :
            product.save()
        return super().save(*args, **kwargs)