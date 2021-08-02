from django.db import models
from django.db.models.base import Model
from .abstract import *


class Fashion(models.Model):
    fashion_name = models.CharField(max_length=100,unique=True,blank=False,null=False)

    def __str__(self):
        return self.fashion_name

class Category(models.Model):
    fashion = models.ForeignKey(Fashion,on_delete=models.CASCADE,related_name="categories")
    category_name = models.CharField(max_length=150)
    def __str__(self):
        return self.category_name
    class Meta:
        unique_together = ['fashion','category_name']
    
   




class ProductSize(models.Model):
    global size_type_choices
    size = models.CharField(max_length=20,unique=True,null=False,blank=False)
    size_type = models.CharField(max_length=20,choices=size_type_choices,default=size_type_choices[0][0])

    def __str__(self):
        return self.size


class Product(DateTimeTracker):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    discount = models.FloatField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    sizes = models.ManyToManyField(ProductSize)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/")
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="colors")
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.color} >> {self.product.title}"
    class Meta:
        unique_together = ['color','product']

class ProductImageGallery(models.Model):
    product_color = models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="products/")



