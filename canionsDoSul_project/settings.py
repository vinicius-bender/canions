from pathlib import Path
import os
from dotenv import load_dotenv

AUTH_USER_MODEL = 'canionsDoSul_app.User'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Carrega o .env baseado na variável DJANGO_ENV
ENV = os.getenv("DJANGO_ENV", "dev")
dotenv_path = BASE_DIR / (".env.prod" if ENV == "prod" else ".env.dev")
load_dotenv(dotenv_path=dotenv_path)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'home'

# SECURITY WARNING: keep the secret key used in production secret!

DEBUG = os.getenv('DEBUG') == 'True'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['31.220.102.180', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'canionsDoSul_app',
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

ROOT_URLCONF = 'canionsDoSul_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'canionsDoSul_app.context_processors.user_roles',
                'canionsDoSul_app.context_processors.breadcrumbs',
            ],
        },
    },
]

WSGI_APPLICATION = 'canionsDoSul_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# settings.py

# URL para acessar os arquivos estáticos
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = '/canions/staticfiles'
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = '/canions/media'
# Para arquivos estáticos em desenvolvimento
if ENV == "prod":
    STATIC_ROOT = '/canions/staticfiles'
    MEDIA_ROOT = '/canions/media'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [
    BASE_DIR / "canionsDoSul_app" / "static",  # Ajuste conforme o nome do seu app
]

# Para produção, se você precisar coletar os arquivos estáticos em um único diretório:
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
