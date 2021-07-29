from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import *


@receiver(post_save,sender=User)
def create_profile(sender,**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        profile = Profile(user=instance)
        profile.save()
        
