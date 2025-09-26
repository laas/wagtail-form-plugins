"""Wagtail hooks for the Nav Buttons plugin."""

from django.templatetags.static import static
from django.utils.html import format_html


def hook_nav_buttons_admin_css() -> str:
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_plugins/nav_buttons/css/form_admin.css"),
    )
