"""Wagtail hooks for the Templating plugin."""

from django.templatetags.static import static
from django.utils.html import format_html


def templating_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_plugins/templating/css/form_admin.css"),
    )
