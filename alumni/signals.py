from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import AlumniProfile

@receiver(post_save, sender=User)
def create_alumni_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Roles.ALUMNI:
        AlumniProfile.objects.create(user=instance)
