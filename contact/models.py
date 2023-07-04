from django.db import models

# Create your models here.
class contactform(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField()
    body = models.TextField()

    def     __str__(self):
        return self.username