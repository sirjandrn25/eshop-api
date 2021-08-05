from django.db import models

from store.models import *
from .abstract import *
# from django.contrib.postgres.fields import JSONField
# from json_field import JSONField


class Cart(DateTimeTracker):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="carts")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    sizes = models.ManyToManyField(ProductSize,blank=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    


class Order(DateTimeTracker):
    status_choices = (
        ('pending','Pending'),
        ('approve','Approve'),
        ('packing','Packing'),
        ('out for deliver','Out for deliver'),
        ('receive','Receive')
    )

    product = models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="orders")
    size = models.ManyToManyField(ProductSize)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    discount = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    is_cancel = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=status_choices,default=status_choices[0][0])

    def __str__(self):
        return f"{self.product.product.title} {self.size} {self.product}"



