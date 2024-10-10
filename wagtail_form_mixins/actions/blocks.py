from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from wagtail import blocks


def validate_emails(value):
    email_variables = ["{author.email}", "{user.email}"]

    for address in value.split(","):
        if address.strip() not in email_variables:
            validate_email(address.strip())


def email_to_block(email_dict):
    email_dict["message"] = email_dict["message"].replace("\n", "</p><p>")
    return {
        "type": "email_to_send",
        "value": email_dict,
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

    class Meta:
        label = _("E-mail to send")


class EmailActionsFormBlock(blocks.StreamBlock):
    email_to_send = EmailsToSendStructBlock()

    class Meta:
        blank = True
