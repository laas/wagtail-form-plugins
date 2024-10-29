from django.utils.html import format_html
from django.templatetags.static import static


def templating_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_form_mixins/templating/css/form_builder.css"),
    )
