from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Registration
print('2222222222')
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('111111')
    if created:
        print('33333333')
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()