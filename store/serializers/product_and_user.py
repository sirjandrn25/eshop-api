from rest_framework.generics import get_object_or_404
from store.models.product_and_user import Cart
from rest_framework import serializers
from store.models import *



class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ['id']
    
    def validate(self,validated_data):
        product = validated_data.get('product')
        user = validated_data.get('user')
        sizes = validated_data.get('sizes')
        if product.colors.all() and sizes is None:
            error = {
                "sizes":["sizes may be required"]
            }
            raise serializers.ValidationError(error)

        if sizes:
            carts = [ cart for cart in Cart.objects.filter(user=user,product=product)]
            for cart in carts:
                if all([True if size in cart.sizes.all() else False for size in sizes]):
                    error = {
                        "detail":["this product is already available in cart"]
                    }
                    raise serializers.ValidationError(error)
            size_types = [size.size.size_type for size in sizes]
            if len(set(size_types))<=1 and len(size_types)>1:
                error= {
                    "sizes":["different size type size may be allowed"]
                }
                raise serializers.ValidationError(error)
            validated_data['sizes'] = sizes
        else:
            cart = Cart.objects.filter(user=user,product=product).first()
        
            if cart:
                error = {
                    "detail":["this product is already availbale in cart"]
                }
                raise serializers.ValidationError(error)
            
            
        return validated_data

