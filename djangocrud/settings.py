from pathlib import Path
import os
import dj_database_url
import dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

AZURE_EXTERNAL_HOSTNAME=os.environ.get('AZURE_HOSTNAME')
if AZURE_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(AZURE_EXTERNAL_HOSTNAME)
RENDER_EXTERNAL_HOSTNAME=os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# Application definition
host = os.environ.get('AZURE_HOSTNAME')
if host:
    CSRF_TRUSTED_ORIGINS = ['https://' + host]
else:
    CSRF_TRUSTED_ORIGINS = []
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "djangocrud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "djangocrud.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

    # Si ocurre una excepción (por ejemplo, si DATABASE_URL no está configurado correctamente),
    # utiliza una configuración de base de datos alternativa
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DATABASE_NAME', 'certificado_factura'),
        'USER': os.environ.get('DATABASE_USER', 'sa'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'Colochampi1234'),
        'HOST': os.environ.get('DATABASE_HOSTNAME', '20.84.115.109'),
        'PORT': os.environ.get('DATABASE_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trust_server_certificate': 'yes',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
LOGIN_URL="/signin/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
    STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    # Ruta a la carpeta 'static' en tu proyecto
    os.path.join(BASE_DIR, 'static'),
]


# CONFIGURACION DE EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "testdjangopruebas@gmail.com"  # Reemplaza con tu dirección de correo electrónico
EMAIL_HOST_PASSWORD = "djangopruebas||11299|"  # Reemplaza con tu contraseña de correo electrónico