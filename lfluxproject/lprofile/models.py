from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')

@receiver(pre_save, sender=User)
def demo_mode_set_superuser(sender, instance, raw, **kwargs):
    if settings.DEMO_MODE:
        instance.is_superuser = True
        instance.is_staff = True

