from django import template
register = template.Library()

class IfGtNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfGtNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = self.var2.resolve(context, True)
        if (self.negate and val1 > val2) or (not self.negate and val1 <= val2):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_ifgt(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])
    return IfGtNode(val1, val2, nodelist_true, nodelist_false, negate)

@register.tag
def ifgt(parser, token):
    """
    Outputs the contents of the block if the first argument is greater than the second.

    Examples::

        {% ifgt user.id comment.user_id %}
            ...
        {% endifgt %}
    """
    return do_ifgt(parser, token, False)
