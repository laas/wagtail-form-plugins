from django.utils.html import format_html
from django.templatetags.static import static


def actions_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_mixins/actions/css/form_builder.css"),
    )
