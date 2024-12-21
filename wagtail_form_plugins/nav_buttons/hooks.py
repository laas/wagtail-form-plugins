from django.utils.html import format_html
from django.templatetags.static import static


def nav_buttons_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_plugins/nav_buttons/css/form_admin.css"),
    )
