from django.db.models import signals
from datetime import datetime, timedelta, date
import reversion


''' convenience methods for reversion-backed models '''

class VersionManagerHelperException(Exception):
    pass


class VersionManagerAccessor(object):
    ''' accessor for history objects, inspired by
        the Django Manager and (Generic)ForeignKey classes

        returns a VersionManager for the object.
    '''

    class VersionManager(object):
        def _translate_reversion_call(self, *args, **kwargs):
            return args.insert(0, self.obj)

        def _proxify_object(self, version):
            ret = self.cls()
            ret.__dict__.update(version.field_dict)
            ret._version = version
            ret.ltools_versiondate = version.revision.date_created
            return ret

        def _proxify_object_s(self, retval):
            ret = None
            try:
                for x in retval:
                    ret = ret or []
                    ret.append(self._proxify_object(x))
            except TypeError, e:
                ret = self._proxify_object(retval)
            return  ret

        def _generate_accessor(self, name, methodname):
            setattr(self, name,
                    lambda *args, **kwargs:
                    self._proxify_object_s(
                        getattr(reversion, methodname)(self.obj, *args, **kwargs)
                        )
                    )


        def __init__(self, obj, cls):
            self.obj = obj
            self.cls = cls

            methods = {'list': 'get_for_object',
                       'for_date': 'get_for_date',
                      }
            for name,methodname in methods.iteritems():
                self._generate_accessor(name, methodname)

        def by_date(self):
            dates = []
            lastdate = None
            vs = self.obj.versions.list()
            vs.sort(key=lambda x: x.ltools_versiondate)
            for versionstory in vs:
                revision = versionstory._version.revision
                if lastdate:
                    while lastdate < revision.date_created.date():
                        lastdate += timedelta(days=1)
                        dates.append((lastdate, [],))
                lastdate = revision.date_created.date()
                if not dates or dates[-1] != lastdate:
                    dates.append((lastdate,[],))
                dates[-1][1].append(versionstory)
            return dates



    def __get__(self, instance, owner):
        if not instance:
            return self
        else:
            return self.VersionManager(instance, owner)

    def _ignore_versioned_modifications(self, instance, sender, **kwargs):
        if instance and hasattr(instance, '_version'):
            raise VersionManagerHelperException("you're trying to overwrite a former version of this model. sorry, that will not work out")


    def contribute_to_class(self, cls, name):
        setattr(cls,name, self)
        signals.pre_delete.connect(self._ignore_versioned_modifications, sender=cls)
        signals.pre_save.connect(self._ignore_versioned_modifications, sender=cls)