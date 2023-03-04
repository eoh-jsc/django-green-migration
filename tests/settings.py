# -*- coding: utf-8 -*-
import os

SECRET_KEY = 'dummy'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sites',
    'green_migration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_EXTENSIONS_DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_EXTENSIONS_DATABASE_NAME', ':memory:'),
        'USER': os.environ.get("DJANGO_EXTENSIONS_DATABASE_USER"),
        'PASSWORD': os.environ.get("DJANGO_EXTENSIONS_DATABASE_PASSWORD"),
        'HOST': os.environ.get('DJANGO_EXTENSIONS_DATABASE_HOST'),
        'PORT': os.environ.get('DJANGO_EXTENSIONS_DATABASE_PORT'),
    }
}

SITE_ID = 1

MEDIA_ROOT = '/tmp/django_extensions_test_media/'

MEDIA_PATH = '/media/'

DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': TEMPLATE_DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_URL = "/static/"
