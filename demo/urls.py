from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail_form_plugins import urls as wfp_urls


urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    *staticfiles_urlpatterns(),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    path("", include(wfp_urls)),
    path("", include(wagtail_urls)),
]
