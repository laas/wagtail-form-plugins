"""Functions used in Wagtail hooks."""

from django.templatetags.static import static
from django.utils.html import format_html


def conditional_fields_admin_css():
    """Inject ConditionalFields-specific css to a Wagtail admin page."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_plugins/conditional_fields/css/form_admin.css"),
    )
