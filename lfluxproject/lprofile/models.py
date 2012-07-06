from django.db import models
from django.contrib.auth.models import User, Group, Permission
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')

@receiver(post_save, sender=User)
def demo_mode_set_permission(sender, instance, created, raw, **kwargs):
    Profile.objects.get_or_create(user=instance)
    g, created = Group.objects.get_or_create(name='editor')
    default_group_perms = [
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='add_story'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='change_story'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='delete_story'),
        ]

    for p in default_group_perms:
        if not p in g.permissions.all():
            g.permissions.add(p)
    if settings.DEMO_MODE and not instance.is_staff:
        instance.groups.add(g)
        instance.is_staff = True
        instance.save()

