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

class SizeSerializer(serializers.ModelSerializer):
    global size_type_choices
    size_type = serializers.ChoiceField(choices=size_type_choices)
    class Meta:
        model = Size
        fields = "__all__"
        read_only_fields = ['id']

class ProductImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageGallery
        fields = "__all__"
        read_only_fields = ['id']

class ProductSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSize
        fields = "__all__"
        read_only_fields = ['id']

class ProductColorSerializer(serializers.ModelSerializer):
    images = ProductImageGallerySerializer(read_only=True,many=True)
    sizes = ProductSizeSerializer(many=True,read_only=True)
    class Meta:
        model = ProductColor
        fields = "__all__"
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    # colors = ProductColorSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id']






