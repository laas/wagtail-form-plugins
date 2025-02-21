"""Web Server Gateway Interface of the demo app."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

application = get_wsgi_application()
