from rest_framework.response import Response
from rest_framework.views import APIView
from store.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class UserSignUpApiView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            # serializer.save()
            user_serializer = UserSerializer(user,many=False)

            return Response(user_serializer.data,status=201)
        else:
            
            return Response(serializer.errors,status=404)


class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            user_serializer = UserSerializer(user,many=False)
            return Response(user_serializer.data,status=200)
        else:
            return Response(serializer.errors,status=404)

class UserApiViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
