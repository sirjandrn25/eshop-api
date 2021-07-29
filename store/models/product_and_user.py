from django.db import models
from django.db.models.fields import related
from store.models import *
from .abstract import *


class Cart(DateTimeTracker):
    product_color = models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="carts")
    size = models.ManyToManyField(ProductSize)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")

    def __str__(self):
        return f"{self.product_color.product.title} {self.size} {self.product_color}"

    class Meta:
        unique_together = ('user','product_color')


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
    