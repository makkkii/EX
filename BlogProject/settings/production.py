from .base import *

ALLOWED_HOSTS = [
    'excurcus.herokuapp.com', 
    'excurcus.xyz', 
    'www.excurcus.herokuapp.com', 
    'www.excurcus.xyz'
]

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

DEFAULT_FROM_EMAIL = 'Excurcus <noreply@excurcus.xyz>'
EMAIL_SUBJECT_PREFIX = '[Excurcus]'