"""Define the ConditionalFieldsFormField data class, representing a field with a rule attribute."""

from dataclasses import dataclass

from wagtail_form_plugins.streamfield.dicts import StreamFieldDataDict, StreamFieldValueDict
from wagtail_form_plugins.streamfield.form_field import StreamFieldFormField

from typing_extensions import Self


class FileInputValueDict(StreamFieldValueDict):
    """A typed dict that holds a stream field value."""

    allowed_extensions: list[str] | None


@dataclass
class FileInputFormField(StreamFieldFormField):
    """Add the rule attribute to the form field object."""

    allowed_extensions: tuple[str] = ("pdf",)

    @classmethod
    def from_streamfield_data(cls, field_data: StreamFieldDataDict) -> Self:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        data = super().from_streamfield_data(field_data)

        field_value: FileInputValueDict = field_data["value"]  # type: ignore[invalid-assignment, reportAssignmentType]
        data.allowed_extensions = field_value.get("allowed_extensions", None)  # type: ignore[reportAttributeAccessIssue]

        return data
