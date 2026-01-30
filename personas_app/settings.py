import os
from pathlib import Path
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

# por defecto no funcional para produccion SECRET_KEY = 'django-insecure-local-app-key-no-secrets-here'

SECRET_KEY = os.getenv('SECRET_KEY', 'yosoyfranchescovirgolinireydecolina01')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CloudSQL proxy para Cloud Run
GCP_PROJECT = os.getenv('GCP_PROJECT', '')

# Supabase Database URL
SUPABASE_DB_URL = os.getenv('DATABASE_URL', '')
IS_RENDER = os.getenv('RENDER', 'false').lower() == 'true'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions', 
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'personas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'personas_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'personas', 'templates')],
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

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/personas_db'),
        conn_max_age=600,
        ssl_require=IS_RENDER  # SSL requiere en Render/Supabase
    ) if os.getenv('DATABASE_URL') else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
]

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'personas', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
