from django.templatetags.static import static
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import EmailsFormBlock, email_to_block
from .dicts import EmailsToSendBlockDict
from .models import EmailActionsFormPage


class EmailActions(Plugin):
    form_page_class = EmailActionsFormPage
    injected_admin_css = format_html(
        '<link rel="stylesheet" href="{href}">',
        href=static("wagtail_form_plugins/emails/css/form_admin.css"),
    )


__all__ = [
    "EmailActions",
    "EmailActionsFormPage",
    "EmailsFormBlock",
    "EmailsToSendBlockDict",
    "email_to_block",
]
