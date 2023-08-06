from .default import *

SECRET_KEY = '{{ params['secret_key'] }}'

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/static_files/'
STATIC_URL = '/static/'

