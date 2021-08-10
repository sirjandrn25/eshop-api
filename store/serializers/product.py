from rest_framework import serializers
from store.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class FashionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True,many=True)
    class Meta:
        model = Fashion
        fields = "__all__"



class ProductImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageGallery
        fields = "__all__"
        read_only_fields = ['id']


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = "__all__"
        read_only_fields = ['id']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = "__all__"
        read_only_fields = ['id']
    def validate(self,validated_data):
        size = validated_data.get('size')
        if type(size) == dict:
            for key in size.keys():
                if type(size[key]) == list:
                    errors = {
                        "size":["only one value is allowed in same type size"]
                    }
                    raise serializers.ValidationError(errors)
            return validated_data
        else:
            errors = {
                'size':['size may be required in json format']
            }
            raise serializers.ValidationError(errors)

class ProductSerializer(serializers.ModelSerializer):
    # colors = ProductColorSerializer(many=True,read_only=True)
    is_available=serializers.BooleanField(default=True)
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id']
    
   
            






