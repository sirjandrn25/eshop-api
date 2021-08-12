
from django.db import models

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
    
   



class Product(DateTimeTracker):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    image = models.ImageField(upload_to="products/")
    is_available = models.BooleanField(default=True)
    is_stock = models.BooleanField(default=True)
    total_stock = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title
   


class ProductColor(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="colors")
    color = models.CharField(max_length=50)
    is_available = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.color} >> {self.product.title}"
    class Meta:
        unique_together = ['color','product']

class ProductSize(models.Model):
    color = models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="sizes")
    size = models.JSONField()
    stock = models.IntegerField(default=1)
    is_stock = models.BooleanField(default=True)
   

    class Meta:
        unique_together = ['color','size']
    
    def __str__(self):
        return f"{self.color.color} {self.size}"
    



class ProductImageGallery(models.Model):
    product_color = models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="products/")



