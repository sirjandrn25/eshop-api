from store.models.product_and_user import Cart
from store.models import *
from rest_framework.viewsets import ModelViewSet
from store.serializers import *



class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer