from rest_framework.viewsets import ModelViewSet
from store.serializers import *
from store.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from store.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication




class CartViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnUser]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()




class OrderViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()