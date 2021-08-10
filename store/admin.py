from store.models.product_and_user import Cart, OrderDetail
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Fashion)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Profile)
# admin.site.register(Size)