from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def make_map(country, field_id):
    try:
        return mark_safe("""<script>
                    WorldMap({'id': '%(field_id)s', padding: 0, zoom: '%(neighbors)s', fgcolor: '#F1F1F1', detail: {'%(country)s': 'black'}});
                  </script>
               """ % {'country': country.ISO.lower(), 'field_id': field_id, 'neighbors': country.neighbours.lower().replace(',li','')}
               )
    except Exception, e:
        print e
        return ""
