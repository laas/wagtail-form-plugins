from typing import Any, TypedDict

from django.utils.html import format_html

from wagtail.models import Page


def format_choices(choices: list, to_html: bool) -> str:
    """Format a list of choices, into html or not."""
    if to_html:
        html_template = f"<ul>{''.join([f'<li>{choice}</li>' for choice in choices])}</ul>"
        return format_html(html_template, choices=choices)
    return "".join([f"\n  • {c}" for c in choices])


class SubmissionData(TypedDict):
    form_data: dict[str, Any]
    page: Page


class StreamFieldValueDict(TypedDict):
    slug: str
    label: str
    help_text: str
    is_required: bool
    initial: str
    disabled: bool


class StreamFieldDataDict(TypedDict):
    id: str
    value: StreamFieldValueDict
    type: str
