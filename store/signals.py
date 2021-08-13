from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from store.models import *


@receiver(post_save,sender=User)
def create_profile(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        profile = Profile(user=instance)
        profile.save()
        


@receiver(pre_save,sender=Product)
def product_pre_signal(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created and instance.total_stock <0:
        instance.total_stock = 0
        instance.is_stock = False
    else:
        colors = instance.colors.all()
        if len(colors):
            # manage the total stock according to product size stock
            total_stock = 0
            for color in colors:
                total_stock += sum([ size.stock for size in color.sizes.all()])
            
            instance.total_stock = total_stock
            if total_stock == 0:
                instance.is_stock = False
            else:
                instance.is_stock = True
            if instance.is_available and all([ color.is_available==False for color in colors]):
                instance.is_available = False

        else:
            if instance.total_stock <=0:
                instance.total_stock = 0
                instance.is_stock = False
            else:
                instance.is_stock = True

@receiver(post_save,sender=Product)
def product_post_signal(sender,**kwargs):
    instance = kwargs.get('instance')
    if instance.is_available is False or instance.is_stock is False:
        for cart in instance.carts.all():
            cart.is_active = False
            cart.save()
    else:
        for cart in instance.carts.all():
            if cart.product_size:
                if cart.product_size.is_stock and cart.quantity <= cart.product_size.stock:
                    cart.is_active = True
                    cart.save()
            else:
                if cart.product.is_available and cart.product.is_stock and cart.product.total_stock >= cart.quantity:
                    cart.is_active = True
                    cart.save()


@receiver(post_save,sender=ProductColor)
def product_color_post_signal(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    
    if created is False:
        # product is not available if all product colors not available
        if instance.is_available == False:

            if all([ color.is_available == False for color in instance.product.colors.all()]):
                instance.product.is_available = False
                instance.product.save()
        else:
            instance.product.is_available = True
            instance.product.save()
            

@receiver(pre_save,sender=ProductSize)
def product_size_pre_signal(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')

    if instance.stock <=0:
        instance.stock = 0
        instance.is_stock = False
    else:
        instance.is_stock = True

@receiver(post_save,sender=ProductSize)
def product_size_post_signal(sender,**kwargs):
    instance = kwargs.get('instance')
    if instance.is_stock:
        instance.color.is_available = True
        instance.color.save()

    else:
        # check all product color sizes if not stock then color is unavailable 
        if all([ size.is_stock == False for size in instance.color.sizes.all()]):
            instance.color.is_available = False
            instance.color.save()
    if instance.is_stock is False:
        for cart in instance.carts.all():
    
            cart.is_active = False
            cart.save()
    else:
        for cart in instance.carts.all():
            if cart.product_size.is_stock and cart.product.is_available and cart.quantity<=cart.product_size.stock:
                cart.is_active = True
                cart.save()

    # all product sizes related stock get and add total stock in product
    product = instance.color.product
    total_stock = 0
    for color in product.colors.all():
        total_stock += sum([ size.stock for size in color.sizes.all()])
    product.total_stock = total_stock
    product.save()
        



@receiver(pre_save,sender=Cart)
def cart_signal(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if instance.is_active:
        if (instance.product.is_stock is False or instance.product.is_available is False ) or (instance.product_size and instance.product_size.is_stock is False):
            instance.is_active = False
    

@receiver(post_save,sender=OrderDetail)
def order_detail_signal(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        if instance.product_size:
            
            instance.product_size.stock = instance.product_size.stock-instance.quantity
            instance.product_size.save()
        else:
            instance.product.total_stock = instance.product.total_stock-instance.quantity
            instance.product.save()


        
