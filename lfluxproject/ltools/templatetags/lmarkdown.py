from django import template
from django.contrib.markup.templatetags.markup import markdown
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter()
def lmarkdown(value, onexception=_(u'Sorry, something is wrong with this text version. We have been notified.')):
    try:
        return markdown(value, 'insparagraph,inmoredetail,extra')
    except ValueError, e:
        print e
        return onexception
