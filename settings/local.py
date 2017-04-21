from .base import *

SECRET_KEY = '5xhsgd$l_2%*)b2a7c$+rx-%h(vh-z2*&y_jx@m4gvqrxsse=2'

DEBUG = True

ALLOWED_HOSTS += (
    "127.0.0.1",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}