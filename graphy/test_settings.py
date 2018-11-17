from graphy.settings import *  # noqa

DEBUG = False

# Use faster password hashing for testing
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
