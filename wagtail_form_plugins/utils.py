"""A set of utility functions used in several places in this project."""

import logging
import re
from collections.abc import Sequence
from html import unescape
from typing import Any
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.core.mail import EmailAlternative, EmailMultiAlternatives
from django.utils.html import format_html, format_html_join, strip_tags
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.utils import get_field_clean_name

LocalBlocks = list[tuple[str, Any]] | None

logging.basicConfig(level=logging.INFO)


def get_logger(file_name: str) -> logging.Logger:
    """Return a logger based on the file name."""
    return logging.getLogger(file_name.split(".", 1)[-1])


LOGGER = get_logger(__file__)


url_regex = (
    r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}"
    r"\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))"
)
email_regex = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
pattern = re.compile(rf"(?P<url>{url_regex})|(?P<email>{email_regex})")


def create_links(html_message: str) -> SafeString:
    """Detect and convert urls into html links."""
    parts = []
    last_end = 0

    for match in pattern.finditer(html_message):
        start, end = match.span()

        if start > last_end:
            parts.append(unescape(html_message[last_end:start]))

        if match.group("url"):
            url = unescape(match.group("url"))
            parts.append(
                format_html('<a href="{url}">{link}</a>', url=quote(url, safe="/:?&#"), link=url),
            )

        elif match.group("email"):
            mail = unescape(match.group("email"))
            parts.append(format_html('<a href="mailto:{mail}">{mail}</a>', mail=mail))

        last_end = end

    if last_end < len(html_message):
        parts.append(unescape(html_message[last_end:]))

    return format_html_join("", "{}", ((p,) for p in parts))


def multiline_to_html(text: str) -> SafeString:
    """Format a multiline text to html."""
    paragraphs = [[create_links(p)] for p in text.strip().splitlines()]
    return format_html_join("\n", "<p>{}</p>", paragraphs)


def format_list(items: Sequence[str | SafeString], bullet: str, *, in_html: bool) -> str:
    """Format a list of items, into html or not."""
    if in_html:
        lists = format_html_join("\n", "<li>{}</li>", [[i] for i in items])
        return format_html("<ul>{lists}</ul>", lists=lists)
    return "".join([f"\n{bullet} {c}" for c in items])


def validate_slug(slug: str) -> None:
    """Validate a slug."""
    if slug != get_field_clean_name(slug):
        raise ValidationError(
            _("Slugs must only contain lower-case letters, digits or underscore."),
        )


def build_email(  # noqa:  PLR0913
    subject: str,
    message: str,
    from_email: str,
    recipient_list: str | list[str],
    reply_to: str | list[str] | None,
    html_message: str | None = None,
) -> EmailMultiAlternatives:
    """Build an email as a EmailMultiAlternatives object."""
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
    """Print an email to the logger - useful for developping."""
    LOGGER.info("=== sending e-mail ===")
    LOGGER.info("subject: %s", email.subject)
    LOGGER.info("from_email: %s", email.from_email)
    LOGGER.info("recipient_list: %s", email.to)
    LOGGER.info("reply_to: %s", email.reply_to)
    LOGGER.info("message: %s", email.body)
    for alternative in email.alternatives:
        if hasattr(alternative, "content"):
            LOGGER.info("html_message: %s", alternative.content)
