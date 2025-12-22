"""
Test settings for Insony
Uses SQLite in-memory database for faster test execution
"""
from .settings import *

# Use SQLite in memory for tests (much faster)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster tests (optional)
# Tests will create tables directly from models
class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None

# Uncomment below to skip migrations (faster but might miss migration issues)
# MIGRATION_MODULES = DisableMigrations()

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use console email backend (don't send real emails)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable debug mode for tests
DEBUG = False

# Use dummy cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Disable template caching
for template in TEMPLATES:
    template['OPTIONS']['debug'] = True

# Static files - use default during tests
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files - use temporary directory
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()