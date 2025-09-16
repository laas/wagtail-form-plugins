"""A set of utility functions used in several places in this project."""

import re
from typing import Any
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.forms.utils import get_field_clean_name

LocalBlocks = list[tuple[str, Any]] | None


def create_links(html_message: str) -> str:
    """Detect and convert urls and emails into html links."""

    def replace_url(match: re.Match[str]):
        return ' <a href="{url}">{link}</a> '.format(
            url=quote(match.group(1), safe="/:?&#"),
            link=match.group(1),
        )

    url_regex = r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))"  # based on https://stackoverflow.com/a/3809435
    email_regex = r"([\w.-]+@[\w.-]+)"

    html_message = re.sub(url_regex, replace_url, html_message)
    return re.sub(email_regex, r'<a href="mailto:\1">\1</a>', html_message)


def validate_identifier(identifier: str):
    if identifier != get_field_clean_name(identifier):
        raise ValidationError(
            _("Identifiers must only contain lower-case letters, digits or underscore."),
        )
