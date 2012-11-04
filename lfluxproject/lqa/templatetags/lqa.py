from django import template
from django.template.loader import render_to_string

from lfluxproject.lqa.forms import QuestionCreateForm

register = template.Library()

class RenderQuestionFormNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()

        if len(tokens) != 3:
            raise template.TemplateSyntaxError("%r tag must have two arguments: 'for' + object" % tokens[0])
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        return cls(obj=parser.compile_filter(tokens[2]))

    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        form = QuestionCreateForm()
        story = self.obj.resolve(context)
        return render_to_string('lqa/_question_form.html', {'form': form, 'story': story}, context_instance=context)

@register.tag
def render_question_form(parser, token):
    return RenderQuestionFormNode.handle_token(parser, token)
