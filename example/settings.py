from pathlib import Path

EXAMPLE_APP_DIR = Path(__file__).parent
BASE_DIR = EXAMPLE_APP_DIR.parent
APP_DIR = BASE_DIR / "wagtail_form_mixins"

# Dev-specific

DEBUG = True
SECRET_KEY = "django-insecure-+7(xh=@&cgu23n$rb*!_^(w5(4&%qwklyr-5iq0!zrjlvs#zso"
ALLOWED_HOSTS = ["*"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTH_PASSWORD_VALIDATORS = []

# Application definition

INSTALLED_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail_form_mixins.actions",
    "wagtail_form_mixins.conditional_fields",
    "wagtail_form_mixins.streamfield",
    "wagtail_form_mixins.templating",
    "example",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "example.urls"
WSGI_APPLICATION = "example.wsgi.application"

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            EXAMPLE_APP_DIR / "templates",
        ],
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

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]

LOCALE_PATHS = [
    APP_DIR / "actions",
    APP_DIR / "conditional_fields",
    APP_DIR / "streamfield",
    APP_DIR / "templating",
]

# Static files

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    EXAMPLE_APP_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# Other Django settings

DEFAULT_AUTO_FIELD =  "django.db.models.BigAutoField"

# Wagtail settings

WAGTAIL_SITE_NAME = "Another form builder example site"
WAGTAILADMIN_BASE_URL = "http://localhost"
WAGTAILDOCS_EXTENSIONS = ['csv', 'pdf', 'txt']

# Forms app settings

FORMS_FROM_EMAIL = "LAAS forms <pi2@laas.fr>"
