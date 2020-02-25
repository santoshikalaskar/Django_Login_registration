from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from datetime import datetime    
# Create your models here.

class Label(models.Model):
    
    labelname = models.CharField("Name_of_label",max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.labelname

class MyNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Name_of_Note",max_length = 500,blank=True)
    note = models.TextField("Enter_note_here")
    image = models.ImageField(blank=True,upload_to="media",null=True)
    is_archieved = models.BooleanField("is_archieved", default=False)
    is_trashed = models.BooleanField("is_trashed", default=False)
    is_pinned = models.BooleanField("is_pinned", default=False)
    remender = models.DateTimeField(blank=True,null=True) 
    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'],blank=True,null=True)
    label = models.ManyToManyField(Label, related_name="label_of_note",blank=True)
    collabrator = models.ManyToManyField(User, related_name="Collabrator_of_note",blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title