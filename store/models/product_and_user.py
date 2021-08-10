from django.db import models
from django.db.models.fields import related

from store.models import *
from .abstract import *
# from django.contrib.postgres.fields import JSONField
# from json_field import JSONField


class Cart(DateTimeTracker):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="carts")
    product_size = models.ForeignKey(ProductSize,on_delete=models.CASCADE,related_name="carts",null=True,default=None,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
        
    


class Order(DateTimeTracker):
    status_choices = (
        ('pending','Pending'),
        ('approve','Approve'),
        ('packing','Packing'),
        ('out for deliver','Out for deliver'),
        ('receive','Receive')
    )
    payment_choices = (
        ('cod',"Cash on Delivery"),
        ("khalti",'Khalti'),
        ("esewa","E-sewa")
    )
    
    address = models.CharField(max_length=150)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    order_status = models.CharField(max_length=50,choices=status_choices,default=status_choices[0][0])
    total_price = models.FloatField()
    contact_no = models.CharField(max_length=20)
    is_payment = models.BooleanField(default=True)
    payment_type = models.CharField(max_length=20,choices=payment_choices,default=payment_choices[0][0])
    is_cancel = models.BooleanField(default=False)




class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_details")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_details")
    product_size = models.ForeignKey(ProductSize,on_delete=models.CASCADE,related_name="order_details",null=True,blank=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    discount = models.FloatField()
    





