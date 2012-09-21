from django.db import models
import django.db.models.options as options
from ltools.markdowntools import pars_to_blocks
import overdiff

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('versioned_attributes',)

def overdiff_and_highlight(old,new):
    def prepare_value(value):
        return pars_to_blocks(value.replace('\r', '').split('\n\n'))

    old = prepare_value(old)
    new = prepare_value(new)
    field_diff_data = list(overdiff.overdiff(old, new))
    field_diffs = []

    for i in xrange(0, len(field_diff_data)):
        field_diffs.append(overdiff.selection_to_s(new[i], field_diff_data[i], markdown=True))
    return '\n\n'.join(field_diffs), len(field_diff_data)>0


"""DIFFTYPES return the new (potentially highlighted) value, plus a boolean value indicating if it changed """
DIFFTYPES = {'=': lambda x,y: (y, x!=y,),
             'd': overdiff_and_highlight
            }

class VersionedContentMixin(models.Model):
    class Meta:
        abstract = True

    def diff_to_older(self, older, override={}):
        results = {}
        for fielddescriptor in self._meta.versioned_attributes:
            extended = ':' in fielddescriptor
            field, difftype = (fielddescriptor,'=',) if not extended else fielddescriptor.split(':')

            fn = DIFFTYPES[difftype] if not difftype in override else override[difftype]
            results[field] = fn(getattr(older,field), getattr(self,field))
        return results
