"""A set of utility functions used in several places in this project."""

import re
from urllib.parse import quote


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
