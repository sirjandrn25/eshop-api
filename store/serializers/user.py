from django.db.models.fields import EmailField
from store.models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,many=False)
    class Meta:
        model = User
        # fields = "__all__"
        read_only_fields = ['id',]
        exclude = ['groups','user_permissions','password']



class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField()
    class Meta:
        model = User
        fields = ('full_name','email','contact_no','password','re_password')
        
    
    def validate(self,validated_data):
        
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        re_password = validated_data.get('re_password','')
        contact_no = validated_data.get('contact_no','')
        full_name = validated_data.get('full_name','')
    
        if email and password and re_password and contact_no and full_name:
            email = User.objects.filter(email=email).first()
            if email:
                error = {
                    'email':['this email id is already exists']
                }
            elif len(contact_no) !=10:
                error = {
                    'contact_no':['10 digits are required']
                }
            elif contact_no.isdigit() is False:
                error = {
                    'contact_no':['only numeric values are allowed']
                }
            elif len(full_name)<6:
                error = {
                    'full_name':['at least 6 charectors are required']
                }
            
            elif len(password)<8:
                error = {
                    'password':['at least 8 charectors are required']
                }
            elif password.isdigit():
                error = {
                    'password':['only numeric values are not allowed']
                }
            elif password !=re_password:
                error = {
                    're_password':['both password is not matched']
                }
            else:
                validated_data.pop('re_password')
                validated_data['password'] = make_password(password)
                user = User.objects.create(**validated_data)
                validated_data['user'] = user
                
                return validated_data

        else:
            error = {
                'email':['this field is required'],
                'full_name':['this field is required'],
                'password':['this field is required'],
                're_password':['this field is required'],
                'contact_no':['this field is required']
            }
        print(error)
        raise serializers.ValidationError(error)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,validated_data):
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user is None:
                errors = {
                    'email':['this email id does not exists']
                }
            elif check_password(password,user.password) is False:
                errors = {
                    'password':["password is not matched"]
                }
            else:
                validated_data['user']=user
                return validated_data

        else:
            errors = {
                'email':['this field is required'],
                'password':['this field is required']
            }
        raise serializers.ValidationError(errors)