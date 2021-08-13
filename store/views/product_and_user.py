from rest_framework.response import Response
from store.models.product_and_user import Cart, OrderDetail
from store.models import *
from rest_framework.viewsets import ModelViewSet
from store.serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from store.permissions import *


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminOrOwnUser]

    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        
        
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
            else:
                obj = self.get_object()
                
                kwargs['data']['user'] = obj.user.id
        return super(CartViewSet,self).get_serializer(*args,**kwargs)
    
   

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrOwnUser]

    def get_serializer(self,*args,**kwargs):
        kwarg_list = list(kwargs.keys())
        
        
        if kwargs.keys() and 'many' not in kwarg_list:
            # kwargs['data']._mutable = True
            if self.request.method == 'POST':
                try:
                    kwargs['data']['user'] = self.request.user.id
                except Exception as e:
                    print(e)
                    kwargs['data']._mutable = True
                    kwargs['data']['user'] = self.request.user.id
            else:
                obj = self.get_object()
                
                kwargs['data']['user'] = obj.user.id
    
        return super(OrderViewSet,self).get_serializer(*args,**kwargs)
    def create_order_detail(self,carts,order):
        for cart in carts:
            order_detail = OrderDetail.objects.create(order=order,product=cart.product,price=cart.product.price,quantity=cart.quantity,product_size=cart.product_size,discount=cart.product.discount)
            cart.delete()   

    def create(self,request):
        carts = request.data.get('carts')
        data = request.data
        data['user'] = request.user.id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            if carts:
                cart_list = []
                for id in carts:
                    try:
                        cart = Cart.objects.get(id=id)
                    except Exception as e:
                        
                        errors = {
                            'carts':["please !!! give valid cart id or pk"]
                        }
                        return Response(errors,status=404)
                    if cart.is_active:
                        cart_list.append(cart)
                if len(cart_list) == 0:
                    errors = {
                        'carts':["please give atleast one active cart"]
                    }
                    return Response(errors,status=404)
                    
            else:
                errors = {
                    'carts':["this must be requireds"]
                }
                return Response(errors,status=404)
            serializer.save()
        
            order_id = serializer.data['id']
            order = Order.objects.get(id=order_id)
            
            self.create_order_detail(carts=cart_list,order=order)
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=404)
    
    @action(detail=True,methods=['get'])
    def details(self,request,pk=None):
        order = get_object_or_404(self.get_queryset(),pk=pk)
        order_details = OrderDetail.objects.filter(order=order)
        serializer = OrderDetailSerializer(order_details,many=True)
        return Response(serializer.data,status=200)


class OrderDetailViewSet(ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]
