"""
Django settings for productsweb project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'modeltranslation',  # обязательно впишите его перед админо
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'simpleapp',
    'django_filters',
    #
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #
    'allauth.socialaccount.providers.yandex',
    #
    'django_apscheduler',
    'celery',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'django.middleware.locale.LocaleMiddleware',  # gettext

    'simpleapp.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'productsweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# Этого раздела может не быть, добавьте его в указанном виде.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'productsweb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##
SITE_ID = 1

STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_REDIRECT_URL = "/products"
##

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Проверяем на подтверждение почты

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

##

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# проверка
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

##

SERVER_EMAIL = os.getenv('SERVER_MAIL')

MANAGERS = (
    ('Ivan', 'a.v.pltnv@gmail.com'),
    ('Petr', 'pltnvntn@yandex.ru'),
)

ADMINS = (
    ('anton', os.getenv('ADMIN_MAIL')),
)
##

EMAIL_SUBJECT_PREFIX = "[WebProducts]"

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
        # 'TIMEOUT': 60
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "formainfo": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] [{levelname}] [{message}]",
            "style": "{",
        },
        "formawarning": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] [{levelname}] [{message}] [{pathname}]",
            "style": "{",
        },
        "formaerorcritical": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] [{levelname}] [{message}] [{pathname}] [{exc_info}]",
            "style": "{",
        },
        "fileloginfo": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] [{levelname}] [{module}] [{message}]",
            "style": "{",
        }
    },
    "handlers": {
        "consoleDebug": {
            "level": "DEBUG",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
            "formatter": "formainfo"
        },
        "consoleWarning": {
            "level": "WARNING",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
            "formatter": "formawarning"
        },
        "consoleErrorCritical": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
            "formatter": "formaerorcritical",
        },

        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_true"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "formawarning",
        },
        "fileInfo": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "fileloginfo",
        },
        "fileErrorCritical": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "errors.log",
            "formatter": "formaerorcritical",
        },
        "fileSecurity": {
            "class": "logging.FileHandler",
            "filename": "security.log",
            "formatter": "fileloginfo",
        },

    },
    "loggers": {
        "django": {
            "handlers": ["consoleDebug", "consoleWarning", "consoleErrorCritical", "fileInfo"],
            "level": "DEBUG",
        },

        "django.request": {
            "handlers": ["fileErrorCritical", "mail_admins"],
            "level": "ERROR",
        },
        "django.server": {
            "handlers": ["fileErrorCritical", "mail_admins"],
            "level": "ERROR",
        },
        "django.template": {
            "handlers": ["fileErrorCritical"],
            "level": "ERROR",
        },
        "django.db.backends": {
            "handlers": ["fileErrorCritical"],
            "level": "ERROR",
        },
        "django.security": {
            "handlers": ["fileSecurity"],
            "level": "DEBUG",
        },
    },
}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]
