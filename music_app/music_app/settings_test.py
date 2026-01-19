"""
Test settings for Insony
Uses SQLite in-memory database for faster test execution
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use console email backend (don't send real emails)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
DEBUG = False
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

for template in TEMPLATES:
    template['OPTIONS']['debug'] = True


STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

import tempfile
MEDIA_ROOT = tempfile.mkdtemp()