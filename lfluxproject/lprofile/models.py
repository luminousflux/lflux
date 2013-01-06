import hashlib
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_apps
from django.contrib.auth.management import create_permissions
from tumblelog.models import ApiKeyProfileMixin


class Profile(UserenaBaseProfile, ApiKeyProfileMixin):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')

    about_me = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)


@receiver(post_save, sender=User)
def demo_mode_set_permission(sender, instance, created, raw, **kwargs):
    if raw:
        return
    try:
        Profile.objects.get_or_create(user=instance)
    except Exception, e:
        print e
        return
    g, created = Group.objects.get_or_create(name='editor')

    # ensure that all Permissions exist. not doing it would break test environments & installation
    for app in get_apps():
        create_permissions(app, None, 2)

    default_group_perms = [
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='add_story'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='change_story'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='story', codename='delete_story'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='stakeholder', codename='add_stakeholder'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='stakeholder', codename='change_stakeholder'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='stakeholder', codename='delete_stakeholder'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='changesuggestion', codename='add_changesuggestion'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='changesuggestion', codename='change_changesuggestion'),
        Permission.objects.get_by_natural_key(app_label='lstory', model='changesuggestion', codename='delete_changesuggestion'),
    ]

    for p in default_group_perms:
        if not p in g.permissions.all():
            g.permissions.add(p)
    if settings.DEMO_MODE and not instance.is_staff:
        instance.groups.add(g)
        instance.is_staff = True
        instance.save()
