"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path, os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.index.apps.IndexConfig',
    'django.contrib.postgres',
    'apps.usuarios.apps.UsuariosConfig',
    'ckeditor',
    'ckeditor_uploader',
    'storages',
    'tinymce'
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Projeto Echos',
        'USER': 'postgres',
        'PASSWORD': str(os.getenv('PASSWORD')),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True



# AWS Configuração

AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))

AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))

AWS_STORAGE_BUCKET_NAME = str(os.getenv('AWS_STORAGE_BUCKET_NAME'))

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_DEFAULT_ACL = 'public-read'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

AWS_LOCATION = 'static'

AWS_QUERYSTRING_AUTH = False

AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
}




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'setup/static')
]

STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_ROOT = os.path.join(BASE_DIR, "imagem_laudo")

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# messages

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR : 'danger',
    messages.SUCCESS : 'success',
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 800,
    'menubar': True,
    'plugins': [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount',
    ],
    'toolbar': 'undo redo | formatselect | ' +
               'bold italic backcolor | alignleft aligncenter ' +
               'alignright alignjustify | bullist numlist outdent indent | ' +
               'removeformat | help',
    'content_css': [
        '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
        '//www.tiny.cloud/css/codepen.min.css',
    ],
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_BASEPATH = "https://cdn.ckeditor.com/4.17.1/standard/"


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar' : 'Custom',
        'height': '500px',
        'width': '200%',
        'toolbar_custom': [
            {'name': 'document', 'groups': ['mode', 'document', 'doctools']},
            {'name': 'clipboard', 'groups': ['clipboard', 'undo']},
            {'name': 'editing', 'groups': ['find', 'selection', 'spellchecker', 'editing']},
            {'name': 'forms', 'groups': ['forms']},
            '/',
            {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
            {'name': 'paragraph', 'groups': ['list', 'indent', 'blocks', 'align', 'bidi', 'paragraph']},
            {'name': 'links', 'groups': ['links']},
            {'name': 'insert', 'groups': ['insert']},
            '/',
            {'name': 'styles', 'groups': ['styles']},
            {'name': 'colors', 'groups': ['colors']},
            {'name': 'tools', 'groups': ['tools']},
            {'name': 'others', 'groups': ['others']},
            {'name': 'about', 'groups': ['about']},
        ],
        
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'autolink lists link',
    'toolbar': 'undo redo | bold italic | bullist numlist | link',
}
