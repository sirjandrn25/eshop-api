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
        


# @receiver(pre_save,sender=Product)
# def product_signal(sender,**kwargs):
    
#     instance = kwargs.get('instance')
#     if instance.total_stock <=0:
#         instance.is_available = False
#         instance.total_stock = 0

#     # adjust the total stock with the help of product size related stock
#     if instance.colors.all():
#         total_stock = 0
#         for color in instance.colors.all():
#             total_stock += sum([size.stock for size in color.sizes.all()])
#         instance.total_stock = total_stock
    
#     # check total stock and check if all product related color is available
#     if instance.total_stock >0 and (all([color.is_available==False for color in instance.colors.all()])== False):
#         instance.is_available = True
    

# @receiver(post_save,sender=Product)
# def product_post_signal(sender,**kwargs):
#     instance = kwargs.get('instance')
#     carts = Cart.objects.filter(product=instance)
#     if instance.is_available == False:
#         for cart in carts:
#             cart.is_active = False
#             cart.save()
#     else:
        
#         # if colors is not present in product then cart is handle
#         if instance.colors.all()==[]:
#             for cart in carts:
#                 cart.is_active = True
#                 cart.save()
#         else:
#             # if colors is present in product then cart is handle 
#             for cart in carts:
#                 if all([size.is_available for size in cart.sizes.all()]):
#                     cart.is_active = True
#                     cart.save()
            
            


        



# @receiver(pre_save,sender=ProductColor)
# def product_color_signal(sender,**kwargs):
#     instance = kwargs.get('instance')
#     created = kwargs.get('created')

    
#     # if all product sizes is unavailable the this sizes related product color is unavailable
#     if (len(instance.sizes.all()) == 0) or all([size.is_available==False for size in instance.sizes.all()]):
#         instance.is_available = False


# @receiver(post_save,sender=ProductColor)
# def product_color_signal(sender,**kwargs):
#     created = kwargs.get('created')
#     instance = kwargs.get('instance')
#     product = instance.product
    
#     # if all product related colors is not available then product is unavailable
#     if all([product_color.is_available==False for product_color in product.colors.all()]) and created is False:
#         product.is_available=False
#         product.save()
#     else:
#         product.is_available = True
#         product.save()



# @receiver(pre_save,sender=ProductSize)
# def productSize_pre_signal(sender,**kwargs):
#     instance = kwargs.get('instance')
#     if instance.stock<=0:
#         instance.is_available = False
#     else:
#         instance.is_available = True

        
        
    

# @receiver(post_save,sender=ProductSize)
# def productSize_post_signal(sender,**kwargs):
#     instance = kwargs.get('instance')
#     item_stocks = [size.stock for size in instance.color.sizes.all()]
#     product = instance.color.product
#     product.total_stock = sum(item_stocks)
#     product.save()
#     color = instance.color
#     if all([size.is_available==False for size in color.sizes.all()]):
#         color.is_available = False
#         color.save()
#     if instance.is_available is False:
#         for cart in Cart.objects.filter(product=instance.color.product):
#             print(cart)
#             if instance in cart.sizes.all():
#                 cart.is_active = False
#                 cart.save()
#     else:
#         if instance.color.product.is_available:
#             carts = [cart for cart in Cart.objects.filter(product=instance.color.product) if instance in cart.sizes.all()]
#             print(carts)
#             for cart in carts:
#                 print([size.is_available for size in cart.sizes.all()])
#                 if all([size.is_available for size in cart.sizes.all()]):
#                     cart.is_active = True
#                     cart.save()




# @receiver(pre_save,sender=Cart)
# def cart_signal(sender,**kwargs):
#     instance = kwargs.get('instance')
#     if instance.sizes.all():
#         if all([size.is_available for size in  instance.sizes.all()]) is False:
#             instance.is_active = False
#     else:
#         if instance.product.is_available is False:
#             instance.is_active = False
        
