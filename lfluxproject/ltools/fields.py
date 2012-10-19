from django.db.models.fields import CharField
from django.conf import settings

import urllib, codecs, os

COUNTRY_INFO_URL = "http://download.geonames.org/export/dump/countryInfo.txt"
COUNTRY_INFO_FILE = os.path.join(settings.SITE_ROOT, 'data/countries.txt')

class Country(object):
    def __init__(self, data):
        super(Country, self).__init__()
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            raise AttributeError()

    @classmethod
    def get_countries(cls):
        """ originally from http://djangosnippets.org/snippets/1049/, modded to return dict """
        try:
            udata = codecs.open(COUNTRY_INFO_FILE, 'r', 'utf-8').read()
        except IOError, e:
            udata = urllib.urlopen(COUNTRY_INFO_URL).read().decode('utf8')
            f = codecs.open(COUNTRY_INFO_FILE, 'w', 'utf-8')
            f.write(udata)
            udata = codecs.open(COUNTRY_INFO_FILE, 'r', 'utf-8').read()

        "Returns a list of dictionaries, each representing a country"
        # Strip the BOM
        if udata[0] == codecs.BOM_UTF8.decode('utf8'):
            udata = udata[1:]
        # Ignore blank lines
        lines = [l for l in udata.split('\n') if l]
        # Find the line with the headers (starts #ISO)
        header_line = [l for l in lines if l.startswith('#ISO')][0]
        headers = header_line[1:].split('\t')
        # Now get all the countries
        country_lines = [l for l in lines if not l.startswith('#')]
        countries = {}
        for line in country_lines:
            country = dict(zip(headers, line.split('\t')))
            countries[country['ISO']] = country
        return countries

    @classmethod
    def countries(cls):
        if not hasattr(cls, '_countries'):
            cls._countries = cls.get_countries()
        return cls._countries

    @classmethod
    def get(cls, iso):
        name = iso.upper()
        countries = cls.countries()
        data = cls(countries[name]) if name in countries else None
        return data

class CountryField(CharField):
    def contribute_to_class(self, cls, name):
        super(CountryField, self).contribute_to_class(cls, name)
        if not self.null:
            setattr(cls, 'get_%s_data' % self.name, lambda modelself: Country.get(getattr(modelself, self.attname)))

try:
    import south
    import south.modelsinspector
    south.modelsinspector.add_introspection_rules([], ["^ltools\.fields\.CountryField"])
except ImportError, e:
    pass

