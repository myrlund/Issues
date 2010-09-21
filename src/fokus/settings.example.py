# Django settings for economy project.

import os
from django.core.urlresolvers import reverse
abspath = lambda p: os.path.join(os.path.dirname(__file__), p).replace('\\','/')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Host, without trailing /
HOST = 'http://example.com'

DATABASES = {
    'default': {
        'NAME': abspath('data.db'),
        'ENGINE': 'sqlite3',
        'USER': '',
        'PASSWORD': '',
    },
    'resources': {
        'NAME': abspath('resources.db'),
        'ENGINE': 'sqlite3',
        'USER': '',
        'PASSWORD': '',
    },
}

DATABASE_ROUTERS = ['fokus.attachment.routers.ResourceRouter',]

ACCEPTED_SHORT = 'godkjent'

INDEXABLE_MODELS = (
    'issue.Issue',
    'update.Update',
    'attachment.ImageResource',
)

APP_TAG = 'Fokus'

EMAIL_SUBJECT_PREFIX = '[%s] ' % APP_TAG 
EMAIL_FROM = '%s <ikke-svar@fokusraad.no>' % APP_TAG

EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

# Maximum update recursion
UPDATE_RECURSION_LIMIT = 5

# Users should be automatically logged in
AUTHENTICATION_BACKENDS = ('fokus.core.backends.CustomBackend',)

# Load user profiles
AUTH_PROFILE_MODULE = 'core.UserProfile'

DATE_FORMAT = "d.m.Y"
TIME_FORMAT = "H:i"

BULLET_COLORS = (
    'red',
    'green',
    'yellow',
    'orange',
    'pink',
    'purple',
    'black',
    'blue',
)

THUMB_SIZE_SMALL = (50, 50)
THUMB_SIZE_NORMAL = (80, 80)

THUMB_SIZE_ISSUE = THUMB_SIZE_NORMAL
THUMB_SIZE_UPDATE = THUMB_SIZE_SMALL

# Path to static files
PATH_STATIC = abspath('static')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = abspath('files') + "/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
#    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 'fokus.issue.helpers.AuthMiddleware',
)

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/user/'

ROOT_URLCONF = 'fokus.urls'

TEMPLATE_DIRS = (
    abspath('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    
    # Thumbnail template filter
    'fokus.nesh.thumbnail',
    
    # Core models
    'fokus.core',
    
    # Issue tracking
    'fokus.issue',
    'fokus.attachment',
    'fokus.update',

    # User handling
    'fokus.user',
    
    # Searching and indexing
    'fokus.search',
    
    # South database migrating tool
    'south',
)
