"""A set a typed dict used for better type hints."""

from datetime import datetime
from typing import Any, TypedDict

from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page


class SubmissionData(TypedDict):
    """A typed dict that holds submision data, typically returned by pre_process_form_submission."""

    form_data: dict[str, Any]
    page: Page


class SubmissionContextDataHeading(TypedDict):
    """A typed dict that holds the header value of a submision context data."""

    name: str
    label: str
    order: str | None


class SubmissionContextDataRow(TypedDict):
    """A typed dict that holds the row value of a submision context data."""

    model_id: str
    fields: list[str | datetime | None]


class SubmissionContextData(TypedDict):
    """A typed dict that holds a submision context data."""

    submissions: list[FormSubmission]
    form_page: Page
    data_headings: list[SubmissionContextDataHeading]
    header_buttons: list[HeaderButton]
    data_rows: list[SubmissionContextDataRow]
    next_url: str
    view: SubmissionsListView


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
