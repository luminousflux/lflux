from django import template

register = template.Library()

@register.filter()
def replace(value, argstr):
    parts = argstr.split(",")
    fromstr = parts[0] if len(parts) >= 1 else ""
    tostr = parts[1] if len(parts) >= 2 else ""
    return value.replace(fromstr, tostr)
