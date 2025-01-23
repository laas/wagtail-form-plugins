from pathlib import Path

DEMO_APP_DIR = Path(__file__).parent
BASE_DIR = DEMO_APP_DIR.parent

# Dev-specific

DEBUG = True
SECRET_KEY = "django-insecure-+7(xh=@&cgu23n$rb*!_^(w5(4&%qwklyr-5iq0!zrjlvs#zso"
ALLOWED_HOSTS = ["*"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTH_PASSWORD_VALIDATORS = []

# Application definition

INSTALLED_APPS = [
    "wagtail_form_plugins",
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
    "django_bootstrap5",
    "demo",
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

ROOT_URLCONF = "demo.urls"
WSGI_APPLICATION = "demo.wsgi.application"

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            DEMO_APP_DIR / "templates",
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

LANGUAGE_CODE = "fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
]

LOCALE_PATHS = [
    DEMO_APP_DIR / "locale",
]

# Static files

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    DEMO_APP_DIR / "static",
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

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Other Django settings

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = ["127.0.0.1"]
AUTH_USER_MODEL = "demo.CustomUser"

# Wagtail settings

WAGTAIL_SITE_NAME = "Wagtail Form Plugin demo website"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"
WAGTAILDOCS_EXTENSIONS = ["csv", "pdf", "txt"]

# Forms app settings

FORMS_FROM_EMAIL = "Wagtail forms <contact@example.com>"
FORMS_FILE_UPLOAD_MAX_SIZE = 10 * 1024 * 1024
FORMS_FILE_UPLOAD_AVAILABLE_EXTENSIONS = ["pdf", "jpg", "jpeg", "png"]
FORMS_VALIDATION_EXPIRATION_DELAY = 60  # 1 hour
FORMS_SUBMISSION_MODEL = "demo.CustomFormSubmission"
FORMS_DEV_SEND_MAIL = False
