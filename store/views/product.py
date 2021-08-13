from django.db.models import query
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from store.models import *
from store.serializers import *
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from store.permissions import *
from store.permissions import *

class FashionViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Fashion.objects.all()
    serializer_class = FashionSerializer
    def destroy(self, request, pk=None):
        fashion = get_object_or_404(Fashion.objects.all(),pk=pk)
        try:
            fashion.delete()
            return Response(status=204)
        except Exception as e:
          
            error = {
                'detail':["can't delete this instance. please first delete this instance related information"]
            }
            return Response(error,status=400)




class CategoryViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category.objects.all(),pk=pk)
        try:
            category.delete()
            return Response(status=204)
        except Exception as e:
            
            error = {
                'detail':["can't delete this instance. please first delete this instance related information"]
            }
            return Response(error,status=400)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    def destroy(self, request, pk=None):
        product = get_object_or_404(Product.objects.all(),pk=pk)
        try:
            product.delete()
            return Response(status=204)
        except Exception as e:
            
            error = {
                'detail':["can't delete this instance. please first delete this instance related information"]
            }
            return Response(error,status=400)
  
    
    @action(detail=True,methods=['get',"post"])
    def colors(self,request,pk=None):
        if request.method == "GET":
            product = get_object_or_404(self.get_queryset(),pk=pk)
            color_list = product.colors.all()
            serializer = ProductColorSerializer(color_list,many=True)
            return Response(serializer.data,status=200)
        elif request.method == "POST":
            data = request.data
            data['product'] = pk
            serializer = ProductColorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            else:
                return Response(serializer.errors,status=404)

        
    
    



class ProductColorViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductColorSerializer
    queryset = ProductColor.objects.all()

    def destroy(self, request, pk=None):
        product_color = get_object_or_404(ProductColor.objects.all(),pk=pk)
        try:
            product_color.delete()
            return Response(status=204)
        except Exception as e:
            
            error = {
                'detail':["can't delete this instance. please first delete this instance related information"]
            }
            return Response(error,status=400)

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
    
        
    @action(detail=True,methods=['get','post'])
    def sizes(self,request,pk=None):
        product_color_obj = self.get_object()
        if request.method == 'POST':
            data = request.data
            data['color'] = pk
            serializer = ProductSizeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            else:
                return Response(serializer.errors,status=404)
        
        serializer = ProductSizeSerializer(product_color_obj.sizes.all(),many=True)
        return Response(serializer.data,status=200)
    
        
            
        

    

class ProductImageGallerViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductImageGallerySerializer
    queryset = ProductImageGallery.objects.all()


class ProductSizeViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSizeSerializer
    queryset = ProductSize.objects.all()


# class SizeViewSet(ModelViewSet):
#     serializer_class = SizeSerializer
#     queryset = Size.objects.all()

#     def destroy(self, request, pk=None):
#         size = get_object_or_404(Size.objects.all(),pk=pk)
#         try:
#             size.delete()
#             return Response(status=204)
#         except Exception as e:

#             error = {
#                 'detail':["can't delete this instance. please first delete this instance related information"]
#             }
#             return Response(error,status=400)




    






    
    