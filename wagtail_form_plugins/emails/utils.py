from typing import TypedDict

from wagtail.rich_text import RichText


class EmailsToSendBlockDict(TypedDict):
    recipient_list: str
    from_email: str
    reply_to: str
    subject: str
    message: str | RichText
