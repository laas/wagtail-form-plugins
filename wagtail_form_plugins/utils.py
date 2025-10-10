"""A set of utility functions used in several places in this project."""

import re
from typing import Any
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.core.mail import EmailAlternative, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.utils import get_field_clean_name

LocalBlocks = list[tuple[str, Any]] | None


def create_links(html_message: str) -> str:
    """Detect and convert urls and emails into html links."""

    def replace_url(match: re.Match[str]) -> str:
        return ' <a href="{url}">{link}</a> '.format(
            url=quote(match.group(1), safe="/:?&#"),
            link=match.group(1),
        )

    url_regex = r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))"  # based on https://stackoverflow.com/a/3809435
    email_regex = r"([\w.-]+@[\w.-]+)"

    html_message = re.sub(url_regex, replace_url, html_message)
    return re.sub(email_regex, r'<a href="mailto:\1">\1</a>', html_message)


def validate_identifier(slug: str) -> None:
    if slug != get_field_clean_name(slug):
        raise ValidationError(
            _("Slugs must only contain lower-case letters, digits or underscore."),
        )


def build_email(
    subject: str,
    message: str,
    from_email: str,
    recipient_list: str | list[str],
    reply_to: str | list[str] | None,
    html_message: str | None = None,
) -> EmailMultiAlternatives:
    if isinstance(recipient_list, str):
        recipient_list = [email.strip() for email in recipient_list.split(",")]
    if isinstance(reply_to, str):
        reply_to = [email.strip() for email in reply_to.split(",")]

    html_message = html_message if html_message else message
    return EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(message.replace("</p>", "\n")),
        from_email=from_email,
        to=recipient_list,
        alternatives=[EmailAlternative(html_message, "text/html")],
        reply_to=reply_to,
    )


def print_email(email: EmailMultiAlternatives) -> None:
    print("=== sending e-mail ===")
    print(f"subject: {email.subject}")
    print(f"from_email: {email.from_email}")
    print(f"recipient_list: {email.to}")
    print(f"reply_to: {email.reply_to}")
    print(f"message: {email.body}")
    for alternative in email.alternatives:
        print(f"html_message: {alternative.content}")  # type: ignore
