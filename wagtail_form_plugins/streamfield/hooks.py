"""Wagtail hooks for the base Streamfield."""

from django.templatetags.static import static
from django.utils.html import format_html


def hook_streamfield_admin_css() -> str:
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_plugins/streamfield/css/form_admin.css"),
    )
