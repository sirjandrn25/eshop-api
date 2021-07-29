from django.db import models
from .abstract import *


class Fashion(DateTimeTracker):
    fashion_name = models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.fashion_name

class Category(DateTimeTracker):
    gender_choices = (
        ('gent',"Gent's"),
        ('women',"Woman's")
    )
    fashion = models.ForeignKey(Fashion,on_delete=models.CASCADE,related_name="categories")
    category_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10,choices=gender_choices,default=gender_choices[0][0])
    

    def __str__(self):
        return self.category_name





class ProductSize(DateTimeTracker):
    size_type_choices = (
        ('int','Int'),
        ('string','String'),
        ('eu','EU'),
        ('Chest','Chest')
    )
    size = models.CharField(max_length=20,primary_key=True)
    size_type = models.CharField(max_length=20,choices=size_type_choices,default=size_type_choices[0][0])

    def __str__(self):
        return self.size


class Product(DateTimeTracker):
    title = models.CharField(max_length=300,primary_key=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    discount = models.FloatField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    sizes = models.ManyToManyField(ProductSize)

    def __str__(self):
        return self.title


class ProductColor(DateTimeTracker):
    global color_choices
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="colors")
    image = models.ImageField(upload_to="products/")
    color = models.CharField(max_length=20,choices=color_choices,default=color_choices[0][0])

    def __str__(self):
        return f"{self.color} >> {self.product.title}"
