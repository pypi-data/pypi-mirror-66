import os

IREKUA_DATABASE_APPS = [
    'django.contrib.postgres',
    'django.contrib.gis',
    'irekua_database',
]

AUTH_USER_MODEL = 'irekua_database.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('IREKUA_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('IREKUA_DATABASE_PORT', '5432'),
        'NAME': os.environ.get('IREKUA_DATABASE_NAME', 'irekua_dummy'),
        'USER': os.environ.get('IREKUA_DATABASE_USER', 'irekua'),
        'PASSWORD': os.environ.get('IREKUA_DATABASE_PASSWORD', ''),
    }
}
