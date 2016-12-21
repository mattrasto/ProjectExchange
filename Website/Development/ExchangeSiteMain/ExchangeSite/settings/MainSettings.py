"""
Django settings for MySite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, '../templates')]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7pigq))=am#fl8ue@=j^47ou@c*zf8dvu+p-v^a!rj9=_y=(9h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']



TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Creates app for model inheritance that only contains global models and admin file
    'ExchangeSite.models',
    'ExchangeSite.apps.guest',
    'ExchangeSite.apps.register',
    'ExchangeSite.apps.login',
    'ExchangeSite.apps.main',
)

SITE_ID = 1


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'ExchangeSite.urls'

WSGI_APPLICATION = 'ExchangeSite.wsgi.application'



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #Contains all website-specific information
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'website',
        'USER': 'root',
        'PASSWORD': '***',
        'HOST': '',
        'PORT': '',
    },
    #Contains all exchange/financial information
    'exchange': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exchange',
        'USER': 'root',
        'PASSWORD': '***',
        'HOST': '',
        'PORT': '',
    }
}

DATABASE_ROUTERS = []



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = None

USE_I18N = True

USE_L10N = True

USE_TZ = False




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
'C:/Programming/Website/DjangoMain/ExchangeSiteMain/ExchangeSite/apps/guest/static',
'C:/Programming/Website/DjangoMain/ExchangeSiteMain/ExchangeSite/apps/register/static',
'C:/Programming/Website/DjangoMain/ExchangeSiteMain/ExchangeSite/apps/login/static',
'C:/Programming/Website/DjangoMain/ExchangeSiteMain/ExchangeSite/apps/main/static',
os.path.join(BASE_DIR, 'static'),
)

STATICFILE_FINDERS = (
"django.contrib.staticfiles.finders.FileSystemFinder",
"django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATIC_ROOT = 'C:/Programming/Website/DjangoMain/ExchangeSiteMain/static/'







