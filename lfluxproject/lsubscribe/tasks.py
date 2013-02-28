from django.conf import settings
from django.utils import translation
from celery.task import task

from .models import Subscription

@task
def send_daily_update():
    translation.activate(settings.LANGUAGE_CODE)
    for subscription in Subscription.objects.filter(frequency='daily',confirmed_at__isnull=False):
        subscription.send_email()

@task
def send_weekly_update():
    translation.activate(settings.LANGUAGE_CODE)
    for subscription in Subscription.objects.filter(frequency='weekly',confirmed_at__isnull=False):
        subscription.send_email()
