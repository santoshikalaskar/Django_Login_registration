from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Label(models.Model):
    
    labelname = models.CharField("Name of label",max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.labelname