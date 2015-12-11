from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['129.1.162.25']

STATIC_ROOT = '/var/www/html/django_static'

STATICFILES_DIRS = (
   # os.path.join(BASE_DIR, "static"),
    '/usr/local/lib/python3.4/dist-packages/rest_framework/static',
    '/usr/local/lib/python3.4/dist-packages/django/contrib/admin/static',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'equestrian',
        'USER': 'hvanhor',
        'PASSWORD': 'Horse',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}
