from django.urls import path

from . import views

urlpatterns = [
    path('images', views.ListCreateImageView.as_view()),
    path('toggle_image',views.ToggleImageView.as_view()),
    path('show_image/<str:image_id>',views.ShowImageView.as_view()),
]