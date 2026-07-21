import os
from pathlib import Path
from dotenv import load_dotenv


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables
load_dotenv(BASE_DIR / ".env")


# Security
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me-in-prod"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"


ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
]


# Applications
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",

    # Local apps
    "app",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    # React frontend communication
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLs
ROOT_URLCONF = "veille_marche_service.urls"


# Templates
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


# WSGI / ASGI
WSGI_APPLICATION = "veille_marche_service.wsgi.application"

ASGI_APPLICATION = "veille_marche_service.asgi.application"


# Database
DB_ENGINE = os.getenv("DB_ENGINE", "postgres").strip().lower()


if DB_ENGINE == "sqlite":

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

elif DB_ENGINE in {"postgres", "postgresql"}:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.getenv(
                "VEILLE_MARCHE_DB_HOST",
                "veille-marche-db"
            ),
            "PORT": os.getenv(
                "VEILLE_MARCHE_DB_PORT",
                "5432"
            ),
            "NAME": os.getenv(
                "VEILLE_MARCHE_DB_NAME",
                "veille_marche_db"
            ),
            "USER": os.getenv(
                "VEILLE_MARCHE_DB_USER",
                "veille_marche_service"
            ),
            "PASSWORD": os.getenv(
                "VEILLE_MARCHE_DB_PASSWORD",
                "veille_marche_service"
            ),
        }
    }

else:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        "DB_ENGINE doit être 'postgres'/'postgresql' ou 'sqlite', "
        f"pas {DB_ENGINE!r}."
    )


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# Internationalization
LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Africa/Casablanca"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = "/static/"


# Media files (images, logos, fichiers uploadés)
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST Framework
#REST_FRAMEWORK = {

  #  "DEFAULT_AUTHENTICATION_CLASSES": (
   #     "rest_framework_simplejwt.authentication.JWTAuthentication",
    #),

   # "DEFAULT_PERMISSION_CLASSES": (
   #     "rest_framework.permissions.IsAuthenticated",
   # ),
#}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# CORS React
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]


# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]


# Security settings production
if not DEBUG:

    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True


# Microservices URLs
# Communication Docker interne (pas localhost)

AUTH_SERVICE_URL = os.getenv(
    "AUTH_SERVICE_URL",
    "http://auth-service:5003"
)


CONFIG_SERVICE_URL = os.getenv(
    "CONFIG_SERVICE_URL",
    "http://config-service:5000"
)
