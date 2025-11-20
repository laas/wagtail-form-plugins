"""A set a typed dict used for better type hints in the Emails plugin."""

from typing import TypedDict

from wagtail.rich_text import RichText


class EmailsToSendBlockDict(TypedDict):
    """A typed dict containing field values in an email form block."""

    recipient_list: str
    from_email: str
    reply_to: str
    subject: str
    message: str | RichText
