from django.db.models import signals
from datetime import datetime, timedelta, date
import reversion
from collections import namedtuple
from difflib import SequenceMatcher


# convenience methods for reversion-backed models


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

        def _proxify_objects(self, retval):
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
                    self._proxify_objects(getattr(reversion, methodname)(self.obj, *args, **kwargs))
                    )

        def __init__(self, obj, cls):
            self.obj = obj
            self.cls = cls

            methods = {'list': 'get_for_object',
                       'for_date': 'get_for_date',
                       }
            for name, methodname in methods.iteritems():
                self._generate_accessor(name, methodname)

        def by_datetime(self):
            vs = self.obj.versions.list()
            return dict([(x._version.revision.date_created, x,) for x in vs])

        def this_date(self):
            return self.obj._version.revision.date_created

        def previous(self):
            current_date = self.obj._version.revision.date_created if hasattr(self.obj, '_version') else None
            versions_by_datetime = self.by_datetime()
            datetimes = versions_by_datetime.keys() if not current_date else [x for x in versions_by_datetime.keys()
                                                                              if x < current_date]
            datetimes.sort()
            if not datetimes:
                return None
            return versions_by_datetime[datetimes[-1]]

        def next(self):
            current_date = self.obj._version.revision.date_created if hasattr(self.obj, '_version') else None
            if not current_date:
                return None
            versions_by_datetime = self.by_datetime()
            datetimes = [x for x in versions_by_datetime.keys() if x > current_date]
            datetimes.sort()
            if not datetimes:
                return None
            return versions_by_datetime[datetimes[0]]

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
                lastdate = revision.date_created.date()
                if not dates or dates[-1] != lastdate:
                    dates.append((lastdate, [], ))
                dates[-1][1].append(versionstory)
            return dict(dates)

        def timeline(self):
            x = self.by_datetime()
            datetimes = sorted(x.keys())
            dates = self.by_date()
            beginning = x[datetimes[0]]._version.revision.date_created.date()
            days = (x[datetimes[-1]]._version.revision.date_created.date() - beginning).days + 1

            Day = namedtuple('Day', ('date', 'events',),)

            result = []

            for i in xrange(days):
                current = beginning + timedelta(days=i)
                if current in dates:
                    result.append(Day(current, dates[current]))
                else:
                    result.append(Day(current, []))
            return result

        def is_current(self):
            if not self.obj:
                raise VersionManagerHelperException("sorry, this is only available for %s instances" % self.cls)
            return not hasattr(self.obj, '_version') or self.for_date(datetime.now())._version == self.obj._version

        def current(self):
            if not self.obj:
                raise VersionManagerHelperException("sorry, this is only available for %s instances" % self.cls)
            if not hasattr(self.obj, '_version'):
                return self.obj
            return self.cls._default_manager.get(pk=self.obj.pk)


        def activity(self):
            diff_overrides = {'d': lambda x,y: SequenceMatcher(a=x,b=y).ratio(), '=': lambda x,y: 0}
            by_date = self.by_date()
            today = date.today()
            activity = []
            for i in xrange(0,-31,-1):
                day = today + timedelta(days=i)
                if day in by_date:
                    current_version = by_date[day][0]
                    previous_version = current_version.versions.previous()
                    amount = 0
                    if not previous_version: # first version, just add a blip.
                        activity.append(100)
                        activity.append(0)
                        activity.append(None)
                        break

                    diffs = current_version.diff_to_older(previous_version, override=diff_overrides)

                    tmp = 0
                    for key,value in diffs.iteritems():
                        length = 0
                        try:
                            length = len(getattr(current_version,key))
                        except ValueError, e:
                            pass # allow for nullable elements
                        tmp+=value*length
                    activity.append(tmp)
                else:
                    activity.append(0)
            return activity[::-1] # reverse



    def __get__(self, instance, owner):
        if not instance:
            return self
        else:
            return self.VersionManager(instance, owner)

    def _ignore_versioned_modifications(self, instance, sender, **kwargs):
        if instance and hasattr(instance, '_version'):
            raise VersionManagerHelperException(
                "you're trying to overwrite a former version of this model. sorry, that will not work out")

    def contribute_to_class(self, cls, name):
        setattr(cls, name, self)
        signals.pre_delete.connect(self._ignore_versioned_modifications, sender=cls)
        signals.pre_save.connect(self._ignore_versioned_modifications, sender=cls)
