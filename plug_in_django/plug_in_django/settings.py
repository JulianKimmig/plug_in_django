import os
import random
import logging

from django.conf import settings
from json_dict import JsonDict
from os.path import expanduser

preamble = ""
#if manage.py is called directly
if len(__name__.split(".")) == 2:
    from manage import logger,CONFIG
else:
    from ..manage import logger,CONFIG
    preamble = __name__.replace(".plug_in_django.settings",".")

BASE_DIR = os.path.join(expanduser("~"), ".plug_in_django")
os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if CONFIG is None:
    os.makedirs(BASE_DIR,exist_ok=True)
    CONFIG = JsonDict(os.path.join(BASE_DIR, "serverconfig.json"))

BASE_DIR = CONFIG.get("django_settings","BASE_DIR",default=BASE_DIR)
if CONFIG.get("django_settings","public_list","settings","BASE_DIR",default=False):
    CONFIG.put("public","settings","BASE_DIR",value=BASE_DIR)

SECRET_KEY = CONFIG.get(
    "django_settings",
    "security",
    "key",
    default="".join(
        random.SystemRandom().choice(
            "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        )
        for i in range(50)
    ),
)

DEBUG = CONFIG.get("django_settings", "DEBUG", default=False)
if CONFIG.get("django_settings","public_list","settings","DEBUG",default=False):
    CONFIG.put("public","settings","DEBUG",value=DEBUG)

ALLOWED_HOSTS = CONFIG.get("django_settings", "security", "ALLOWED_HOSTS", default=[])
if CONFIG.get("django_settings","public_list","settings","ALLOWED_HOSTS",default=False):
    CONFIG.put("public","settings","ALLOWED_HOSTS",value=ALLOWED_HOSTS)

LANGUAGE_CODE = CONFIG.get("django_settings", "language_time", "LANGUAGE_CODE", default="en-us")
if CONFIG.get("django_settings","public_list","settings","LANGUAGE_CODE",default=True):
    CONFIG.put("public","settings","LANGUAGE_CODE",value=LANGUAGE_CODE)

TIME_ZONE = CONFIG.get("django_settings", "language_time", "TIME_ZONE", default="UTC")
if CONFIG.get("django_settings","public_list","settings","TIME_ZONE",default=True):
    CONFIG.put("public","settings","TIME_ZONE",value=TIME_ZONE)


USE_I18N = CONFIG.get("django_settings", "language_time", "USE_I18N", default=True)
if CONFIG.get("django_settings","public_list","settings","USE_I18N",default=False):
    CONFIG.put("public","settings","USE_I18N",value=USE_I18N)

USE_L10N = CONFIG.get("django_settings", "language_time", "USE_L10N", default=True)
if CONFIG.get("django_settings","public_list","settings","USE_L10N",default=False):
    CONFIG.put("public","settings","USE_L10N",value=USE_L10N)

USE_TZ = CONFIG.get("django_settings", "language_time", "USE_TZ", default=True)
if CONFIG.get("django_settings","public_list","settings","USE_TZ",default=False):
    CONFIG.put("public","settings","USE_TZ",value=USE_TZ)


STATIC_URL = CONFIG.get("django_settings", "static_files", "url", default="/static/")


INSTALLED_APPS = []

if CONFIG.get("django_settings", "apps", "load_defaults", default=True):
    INSTALLED_APPS += [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        'bootstrap4',
    ]

INSTALLED_APPS += CONFIG.get("django_settings", "apps", "additional", default=[])

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] + CONFIG.get(
    "django_settings", "static_files", "dirs", default=[]
)


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "global_login_required.GlobalLoginRequiredMiddleware",
]

PUBLIC_PATHS = [r"^/accounts/.*"]  # allow public access to all django-allauth views
ROOT_URLCONF = preamble + "controll_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                preamble + "templatetags.installed_apps.get_apps_context",
                ],
            "libraries": {"public_dict": preamble + "templatetags.public_dict"},
        },
    }
]

WSGI_APPLICATION = preamble + "controll_server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":  CONFIG.get(
            "django_settings",
            "database",
            "name",
            default=os.path.abspath(os.path.join(os.path.dirname(CONFIG.file), "db.sqlite3")),
        )
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
