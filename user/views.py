from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer, LoginSerializer, RegisterSerializer, AuthSerializer

class ListCreateUserView(ListCreateAPIView):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
      return User.objects.all()

    def create(self, request, *args, **kwargs):
      if RegisterSerializer(data=request.data).is_valid():
        username = request.data['username']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        if (password != confirm_password):
          return JsonResponse({
            'message': 'Invalid Password!'
          }, status=status.HTTP_400_BAD_REQUEST)

        if username != '' and password != '':
            user = User.objects.create_user(
              username=username, 
              password=password
            )
            return JsonResponse({
                'message': 'Create a new User successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new User unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def get_serializer(self, *args, **kwargs):
      return LoginSerializer(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
      try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)

        user_ser = UserSerializer(user)
        if user_ser:
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = authenticate(username=username, password=password)
          update_last_login(None, user)
          data = AuthSerializer(user).data
          return JsonResponse({
              'message' : "success",
              'data': data
          }, status=200)
        else:
          return JsonResponse({'message' : "user does not exists"}, status=401)
      except Exception as ex:
        return JsonResponse({'message' : str(ex)}, status=401)