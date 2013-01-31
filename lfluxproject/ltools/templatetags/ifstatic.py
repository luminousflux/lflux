from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.storage import staticfiles_storage
register = template.Library()

class IfStaticNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')
    def __init__(self, var1, nodelist_true, nodelist_false, negate):
        self.var1 = var1
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfStaticNode>"

    def render(self, context):
        context.push()
        val1 = self.var1.resolve(context, True)
        context['static'] = static(val1)
        print context['static']

        print val1
        if staticfiles_storage.exists(val1):
            x = self.nodelist_true.render(context)
        else:
            x = self.nodelist_false.render(context)
        context.pop()
        return x

def do_ifstatic(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    return IfStaticNode(val1, nodelist_true, nodelist_false, negate)

@register.tag
def ifstatic(parser, token):
    """
    Outputs the contents of the block if the static file exists

    Examples::

        {% ifstatic 'static.ext' %}
            ...
            {{static}}
        {% else %}
        {% endifstatic %}
    """
    return do_ifstatic(parser, token, False)
