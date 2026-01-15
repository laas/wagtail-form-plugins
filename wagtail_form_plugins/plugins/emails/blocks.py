"""Blocks definition for the Emails plugin."""

from typing import Any

from django.conf import settings
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from wagtail_form_plugins.utils import LocalBlocks

from .dicts import EmailsToSendBlockDict


def email_to_block(email_dict: EmailsToSendBlockDict) -> dict[str, Any]:
    """Return a dict that can be used to fill an email form block based on an email dict."""
    email_dict["message"] = str(email_dict["message"]).replace("\n", "</p><p>")
    return {
        "type": "email_to_send",
        "value": email_dict,
    }


class EmailsToSendStructBlock(blocks.StructBlock):
    """Wagtail struct block used to define one email entry."""

    recipient_list = blocks.CharBlock(
        label=_("Recipient list"),
        help_text=_("E-mail addresses of the recipients, separated by comma."),
    )

    from_email = blocks.CharBlock(
        required=False,
        label=_("From"),
        help_text=_("E-mail addresses set in the “from” email field, separated by comma."),
        default=settings.FORMS_FROM_EMAIL,
    )

    reply_to = blocks.CharBlock(
        required=False,
        label=_("Reply to"),
        help_text=_("E-mail addresses set in the “reply_to” email field, separated by comma."),
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


class EmailsFormBlock(blocks.StreamBlock):
    """Wagtail stream block used to manage form emails behavior."""

    email_to_send = EmailsToSendStructBlock()

    def validate_email(self, field_value: str) -> None:
        """Validate the email addresses field value. Extend it to personalize email validation."""
        for email in field_value.split(","):
            validate_email(email.strip())

    def __init__(self, local_blocks: LocalBlocks = None, search_index: bool = True, **kwargs):  # noqa: FBT001, FBT002
        super().__init__(local_blocks, search_index, **kwargs)

        for child_block in self.__class__.declared_blocks.values():  # ty: ignore unresolved-attribute
            child_block.child_blocks["recipient_list"].field.validators = [self.validate_email]
            child_block.child_blocks["reply_to"].field.validators = [self.validate_email]
            child_block.child_blocks["from_email"].field.validators = [self.validate_email]

    class Meta:
        blank = True
