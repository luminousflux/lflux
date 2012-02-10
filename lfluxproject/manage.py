#!/usr/bin/env python
from django.core.management import execute_manager
import imp
import os,sys

SETTINGSMODULE = os.environ.get('DJANGO_SETTINGS_MODULE', None) or 'settings'

sys.path.append(os.path.abspath(os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.pardir)))

mpaths = SETTINGSMODULE.rsplit('.',1)
mpath = mpaths[0]
mfrom = [mpaths[1]] if len(mpaths)>1 else []

modobj = None

try:
    modobj = __import__(SETTINGSMODULE, fromlist=mfrom)
except ImportError, e:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(modobj)
