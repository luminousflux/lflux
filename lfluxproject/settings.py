gettext = lambda s: s
INTERNAL_IPS = ('127.0.0.1',)
TIME_ZONE = 'Europe/Vienna'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
)
ROOT_URLCONF = 'lfluxproject.urls'


# from http://morethanseven.net/2009/02/11/django-settings-tip-setting-relative-paths.html
import os
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'localstatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)
LOCALE_PATHS = (os.path.join(SITE_ROOT,'conf/locale'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django_nose',
    'django_extensions',

    'debug_toolbar',
    'ltools',           # overrides some django templates
    'pagedown',
    'south',
    'taggit',
    'reversion',
    'crispy_forms',     # for tumblelog
    'tumblelog',
    'userena',
    'guardian',         # for userena
    'easy_thumbnails',  # for userena

    'lstory',
    'limage',
    'lprofile',
    'ladmin',           # admin overrides & extensions.
    'lqa',

    'voting',
    'threadedcomments',
    'google_analytics',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',  # required by django-admin-tools
    'lfluxproject.context_processors.settings_processor',
    'lfluxproject.context_processors.tracking_processor',
    'lfluxproject.context_processors.site_processor',
    'lfluxproject.context_processors.flatcontent',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
ADMIN_TOOLS_INDEX_DASHBOARD = {
    'ladmin.admin.admin': 'lfluxproject.dashboard.CustomIndexDashboard',
    'django.contrib.admin.site': 'admin_tools.dashboard.DefaultIndexDashboard'
}
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
CRISPY_TEMPLATE_PACK = 'uni_form'
COMMENTS_APP = 'threadedcomments'
TUMBLELOG_PARENT_MODEL = 'lstory.Story'
ANONYMOUS_USER_ID = -1  # required by guardian?
AUTH_PROFILE_MODULE = 'lprofile.Profile'
LOGIN_URL = '/user/signin/'
LOGOUT_URL = '/user/signout/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_SIGNIN_REDIRECT_URL = '/user/%(username)s/'
SOUTH_TESTS_MIGRATE = False
TUMBLELOG_TYPEIMAGES = True



# Customize your config here.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# you should change this in your local settings.
EMBEDLY_KEY = None # OVERRIDE THIS
EMBEDLY_MAXWIDTH = 300
GOOGLE_ANALYTICS_ACCOUNT_CODE = False
SECRET_KEY = ''                         # Make this unique, and don't share it with anybody.


DEMO_MODE = False                       # make all users editors per default

try:                                    # import all settings from local_settings. we recommend setting DJANGO_SETTINGS_MODULE environment variable and importing from here instead, so one can f.e. change INSTALLED_APPS
    from local_settings import *
except ImportError:
    pass
