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
        data: Self = super().from_streamfield_data(field_data)

        class FileInputValueDict(StreamFieldValueDict):
            allowed_extensions: tuple[str]

        field_value: FileInputValueDict = field_data["value"]  # ty: ignore invalid-assignment
        allowed_extensions = field_value.get("allowed_extensions", ())
        data.allowed_extensions = allowed_extensions

        return data
