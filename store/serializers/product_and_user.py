from copy import error
from rest_framework.generics import get_object_or_404
from store.models.product_and_user import Cart, Order
from rest_framework import serializers
from store.models import *



class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ['id']
    
    def validate(self,validated_data):
        product_size = validated_data.get('product_size')
        product = validated_data.get('product')
        user = validated_data.get('user')
        quantity = validated_data.get('quantity')

        if quantity:
            if type(quantity) == int:
                if quantity<=0:
                    validated_data['quantity'] = 1
            else:
                errors = {
                    "quantity":["quantity may be required in integer value"]
                }
                raise serializers.ValidationError(errors)

        if product_size:
            cart = Cart.objects.filter(user=user,product=product,product_size=product_size).first()
            if cart:
                errors = {
                    "cart":['this cart is already exists']
                }
                raise serializers.ValidationError(errors)
            if quantity> product_size.stock:
                errors = {
                    "quanity":["quantity may not be greater than product stock"]
                }
                raise serializers.ValidationError(errors)
        else:
            cart = Cart.objects.filter(user=user,product=product).first()
            if cart:
                errors = {
                    "cart":['this cart is already exists']
                }
                raise serializers.ValidationError(errors)
            
            if quantity> product.total_stock:
                errors = {
                    "quanity":["quantity may not be greater than product stock"]
                }
                raise serializers.ValidationError(errors)
        

        return validated_data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['id']

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"
        read_only_fields = ["id"]
        