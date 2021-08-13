from django.http import request
from rest_framework.response import Response
from rest_framework.views import APIView
from store.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from store.permissions import *

class UserSignUpApiView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            user_serializer = UserSerializer(user,many=False)

            return Response(user_serializer.data,status=201)
        else:
            
            return Response(serializer.errors,status=404)


class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            
            refresh = RefreshToken.for_user(user)
            resp = {
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':user.id
            }
            return Response(resp,status=200)
        else:
            return Response(serializer.errors,status=404)

class UserApiViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminOrOwnUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    @action(detail=True,methods=['put'])
    def profile(self,request,pk=None):
        user = get_object_or_404(User.objects.all(),pk=pk)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data,status=200)
        else:
            return Response(serializer.errors,status=404)
    
    @action(detail=True,methods=["get"],permission_classes=[IsAuthenticated,IsAdminOrOwnUser])
    def orders(self,request,pk=None):
        user = get_object_or_404(self.get_queryset(),pk=pk)
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data,status=200)
    
    @action(detail=True,methods=["get"],permission_classes=[IsAuthenticated,IsAdminOrOwnUser])
    def carts(self,request,pk=None):
        user = get_object_or_404(self.get_queryset(),pk=pk)
        carts = Cart.objects.filter(user=user)
        serializer = CartSerializer(carts,many=True)
        return Response(serializer.data,status=200)
    
    @action(detail=True,methods=['delete'],permission_classes=[IsAuthenticated,IsAdminOrOwnUser])
    def clear_carts(self,request,pk=None):
        user = get_object_or_404(self.get_queryset(),pk=pk)
        carts = Cart.objects.filter(user=user)
        for cart in carts:
            cart.delete()
        return Response(status=204)




class UserLogoutApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        refresh = request.data.get('refresh')
        if refresh:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=200)
        else:
            resp = {
                "refresh":["this field is required"]
            }
            return Response(resp,status=404)



