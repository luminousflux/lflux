import overdiff
import collections
from django.db import models
import django.db.models.options as options
from ltools.markdowntools import pars_to_blocks
#from ltools.managers import VersionManagerAccessor

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

def _recurse_diff(old,new):
    result = []
    for x in new:
        matching = [o for o in old if o.pk == x.pk]
        result.append(x.diff_to_older(matching[0]) if matching else x.diff_to_older(None))
    return result

#"""DIFFTYPES return the new (potentially highlighted) value, plus a boolean value indicating if it changed """
DIFFTYPES = {'=': lambda x,y: (y, x!=y,),
             'd': overdiff_and_highlight,
             'r': _recurse_diff,
            }

class VersionedContentMixin(models.Model):
    #versions = VersionManagerAccessor()
    #objects = models.Manager()
    class Meta:
        abstract = True

    def diff_to_older(self, older, override={}):
        results = {}
        for fielddescriptor in self._meta.versioned_attributes:
            extended = ':' in fielddescriptor
            field, difftype = (fielddescriptor,'=',) if not extended else fielddescriptor.split(':')
            if difftype=='r':
                field+='_'

            # call if callable
            cic = lambda x: x() if isinstance(x, collections.Callable) else x
            # get and call
            gac = lambda model, field: cic(getattr(model, field))

            fn = DIFFTYPES[difftype] if not difftype in override else override[difftype]
            if older:
                results[field] = fn(gac(older,field), gac(self,field))
            else:
                results[field] = fn('', gac(self, field))
        return results
