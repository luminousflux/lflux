from django import template
import tldextract
register = template.Library()

@register.filter('tldextract')
def tldextract_filter(value):
    return ('.'.join([x for x in tldextract.extract(value) if x!='www'])).strip('.')
