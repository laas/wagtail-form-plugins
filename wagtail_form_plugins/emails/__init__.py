from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import EmailsFormBlock, email_to_block
from .hooks import hook_emails_admin_css
from .models import EmailActionsFormPage


class EmailActions(Plugin):
    form_page_class = EmailActionsFormPage


__all__ = [
    "EmailActions",
    "EmailActionsFormPage",
    "EmailsFormBlock",
    "email_to_block",
    "hook_emails_admin_css",
]
