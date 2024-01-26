from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from image.models import Image
from image.serializers import ImageSerializer
from .forms import ImageForm

class ListCreateImageView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    model = Image
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.all()

    def create(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()      
            return JsonResponse({
                'message': 'Create a new Image successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Image unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class ToggleImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
      id = request.data['id']
      new_status = not Image.objects.get(id=id).active
      image = Image.objects.filter(id=id).update(active=new_status)

      return JsonResponse({
              'message': 'Toggle Image successful!'
          }, status=status.HTTP_201_CREATED)

class ShowImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id,*args, **kwargs):
      image = Image.objects.get(id=image_id)
      if (image.active == False):
        return JsonResponse({
            'message': 'Image Not Found!'
        }, status=status.HTTP_404_NOT_FOUND)
      serializer = ImageSerializer(image)
      return JsonResponse({
          'message' : 'success',
          'data': serializer.data
        }, status=status.HTTP_201_CREATED)    