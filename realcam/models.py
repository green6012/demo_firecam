from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Camera(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Warning(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Camera, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='warning_images', blank=True, null=True)