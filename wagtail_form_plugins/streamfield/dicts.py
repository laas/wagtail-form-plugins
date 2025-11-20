"""A set a typed dict used for better type hints."""

from typing import Any, TypedDict

from wagtail.models import Page


class SubmissionData(TypedDict):
    """A typed dict that holds submision data, typically returned by pre_process_form_submission."""

    form_data: dict[str, Any]
    page: Page


class StreamFieldValueDict(TypedDict):
    """A typed dict that holds a stream field value."""

    slug: str
    label: str
    help_text: str
    is_required: bool
    initial: str
    disabled: bool


class StreamFieldDataDict(TypedDict):
    """A typed dict that holds a stream field data."""

    id: str
    value: StreamFieldValueDict
    type: str
