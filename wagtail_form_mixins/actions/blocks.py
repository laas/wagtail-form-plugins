from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from wagtail import blocks


def validate_emails(value):
    email_variables = ['{author_email}', '{user_email}']

    for address in value.split(","):
        if address.strip() not in email_variables:
            validate_email(address.strip())


class Email:
    def __init__(self, recipient_list: str, subject: str, message: str):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

    def format(self):
        return {
            "type": "email_to_send",
            "value": {
                "recipient_list": self.recipient_list,
                "subject": self.subject,
                "message": self.message.replace('\n','</p><p>'),
            }
        }


class EmailsToSendStructBlock(blocks.StructBlock):
    recipient_list = blocks.CharBlock(
        label=_("Recipient list"),
        validators=[validate_emails],
        help_text=_("E-mail addresses of the recipients, separated by comma."),
    )

    subject = blocks.CharBlock(
        label=_("Subject"),
        help_text=_("The subject of the e-mail."),
    )

    message = blocks.RichTextBlock(
        label=_("Message"),
        help_text=_("The body of the e-mail."),
    )


class EmailActionsFormBlock(blocks.StreamBlock):
    email_to_send = EmailsToSendStructBlock()
