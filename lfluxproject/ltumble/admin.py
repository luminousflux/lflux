from django.contrib import admin
from lstory.admin import StoryAdmin

StoryAdmin.inlines = StoryAdmin.inlines or []

from tumblelog.admin import PostTypeAdmin
from tumblelog.settings import POST_TYPES
from tumblelog.util import import_from

class PostTypeInline(admin.StackedInline):
    max_num = 1

for post_type in POST_TYPES:
    model = import_from(post_type)
    admin_cls = type(PostTypeInline.__name__,
            (PostTypeInline,),
            {})
    admin_cls.model = model
    StoryAdmin.inlines.append(admin_cls)
