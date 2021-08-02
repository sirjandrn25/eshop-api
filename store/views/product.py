from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from store.models import *
from store.serializers import *
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from store.permissions import *

class FashionViewSet(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    queryset = Fashion.objects.all()
    serializer_class = FashionSerializer


class CategoryViewSet(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]

    @action(detail=True,methods=['put'])
    def sizes(self,request,pk=None):
        size = request.data.get('size')
        if size:
            product_size = ProductSize.objects.get(id=size)
            product = get_object_or_404(self.get_queryset(),pk=pk)
            exist_size_list = [product_size.id for product_size in product.sizes.all() if ((product_size.id == size) or (product_size.size == size))]
            if exist_size_list:
            
                product.sizes.remove(product_size)
                serializer = ProductSerializer(product)
                return Response(serializer.data,status=201)
            else:
                product.sizes.add(product_size)
                serializer = ProductSerializer(product)
                return Response(serializer.data,status=200)
        else:
            resp = {
                'size':["this field is required"]
            }
            return Response(resp,status=404)
    @action(detail=True,methods=['get'])
    def colors(self,request,pk=None):
        product = get_object_or_404(self.get_queryset(),pk=pk)
        color_list = product.colors.all()
        serializer = ProductColorSerializer(color_list,many=True)
        return Response(serializer.data,status=200)


class ProductSizeViewSet(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    



class ProductColorViewSet(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    serializer_class = ProductColorSerializer
    queryset = ProductColor.objects.all()

    @action(detail=True,methods=["get","post"])
    def images(self,request,pk=None):
        product_color = get_object_or_404(self.get_queryset(),pk=pk)
        if request.method=="POST":
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    image_obj = ProductImageGallery.objects.create(product_color=product_color,image=image)

            else:
                resp = {
                    "images":["this field must required"]
                }
                return Response(resp,status=404)
      
        serializer = ProductImageGallerySerializer(product_color.images.all(),many=True)
        return Response(serializer.data,status=200)

    
class ProductImageGallerViewSet(ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    serializer_class = ProductImageGallerySerializer
    queryset = ProductImageGallery.objects.all()



    






    
    