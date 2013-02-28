from django.contrib import admin

from .models import *
from .forms import *

class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm
admin.site.register(Subscription, SubscriptionAdmin)
