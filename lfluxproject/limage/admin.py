from django.contrib import admin
from django.db import models
import reversion
from django_markdown.widgets import MarkdownWidget

from models import Image

admin.site.register(Image)
