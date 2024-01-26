from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import User
from user.models import AccessToken

class UserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ('id','username','last_login')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)


class AccessTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessToken
        fields = '__all__'


class AuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username','auth_token')
    
    def get_auth_token(self, obj):
        token,_ = Token.objects.get_or_create(user=obj)
        return token.key