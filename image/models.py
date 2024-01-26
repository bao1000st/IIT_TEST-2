from django.db import models
from django.contrib.auth.models import User
import uuid


class ImageManager(models.Manager):
    def create_image(self, **kwargs):
      invoice = self.model(**kwargs)
      invoice.save()
      return invoice
    
    
class Image(models.Model):
    img = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(null=False,auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    active =  models.BooleanField(null=False,default=True)
    
    objects = ImageManager()