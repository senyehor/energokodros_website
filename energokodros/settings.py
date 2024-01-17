import os.path
from pathlib import Path

import environ
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy

env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env('DEBUG')
# random secret key to collect static during docker build
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [] if DEBUG else env('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    'users',
    'energy',
    'institutions',
    'utils',

    'crispy_forms',
    'active_link',
    'treebeard',
    'formtools',
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

ROOT_URLCONF = 'energokodros.urls'

AUTHENTICATION_BACKENDS = [
    'users.backends.AllowTryAuthenticateInactive',
]

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.user_roles_applications_to_review_count'
            ],
        },
    },
]

WSGI_APPLICATION = 'energokodros.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     env('DB_NAME'),
        'USER':     env('DB_USERNAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST':     env('DB_HOST'),
        'PORT':     env('DB_PORT'),
    }
}

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

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True
# enable using timedelta objects to set session expiration time
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [os.path.join(BASE_DIR, STATIC_URL)]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = LOGIN_URL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIN_HASH_LENGTH = env.int('MIN_HASH_LENGTH')

DEFAULT_PAGINATE_BY = env.int('DEFAULT_PAGINATE_BY')

SENSOR_COUNT_PER_BOX = env.int('SENSORS_COUNT_PER_BOX')

ACTIVE_LINK_STRICT = True

LOGGING = {
    "version":                  1,
    "disable_existing_loggers": False,
    "root":                     {"level": "INFO", "handlers": ["console"]},
    "handlers":                 {
        "console": {
            "level":     "INFO",
            "class":     "logging.StreamHandler",
            "formatter": "app",
        },
    },
    "loggers":                  {
        "django": {
            "handlers":  ["console"],
            "level":     "INFO",
            "propagate": True
        },
    },
    "formatters":               {
        "app": {
            "format":  (
                "%(asctime)s [%(levelname)s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}
