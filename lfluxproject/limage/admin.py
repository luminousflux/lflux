from django.contrib import admin
from django.db import models
import reversion

from models import Image

admin.site.register(Image)
