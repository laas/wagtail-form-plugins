from typing import Any, TypedDict

from wagtail.models import Page


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
