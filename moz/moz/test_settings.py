SECRET_KEY = 'fake-key'

ROOT_URLCONF = 'moz.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'phonenumber_field',
    'languages',
    'geo.apps.GeoConfig',
    'rest_framework',
    'rest_framework_gis',
    'djmoney',
    'djmoney.contrib.exchange',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mbcp_db',
        'USER': 'mbcp_user',
        'PASSWORD': 'xsq3SHWtR82Cu9Ca6s',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'mbcp_tests',
        }
    }
}

EXCHANGE_BACKEND = 'moz.utils.TestExchangeBackend'
