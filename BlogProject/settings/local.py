from .base import *


ALLOWED_HOSTS = []
DEBUG = True
SECRET_KEY =  'uyo%o40+mdpc$630p5y=t0p*=pm6lhdzplyvd^*h$86+xq_98l'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'