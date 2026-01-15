"""Define the StreamFieldFormField data class, representing a field."""

from dataclasses import dataclass

from wagtail.contrib.forms.utils import get_field_clean_name

from .dicts import StreamFieldDataDict

from typing_extensions import Self


@dataclass
class WaftailFormField:
    """
    A dataclass containing field attributes used by wagtail.

    Such as in FormMixin.get_data_fields,
    FormBuilder.formfields(), FormBuilder.get_field_options(), and in first attribute of all
    create_field methods.
    """

    clean_name: str
    field_type: str
    label: str
    help_text: str
    required: bool
    choices: list[tuple[str, str]]
    default_value: str | list[str]


@dataclass
class StreamFieldFormField(WaftailFormField):
    """A data class representing a field with some extra attributes and syntactic sugar."""

    block_id: str
    disabled: bool

    @property
    def slug(self) -> str:
        """Alias for clean_name attribute."""
        return self.clean_name

    @property
    def type(self) -> str:
        """Alias for field_type attribute."""
        return self.field_type

    @classmethod
    def from_streamfield_data(cls, field_data: StreamFieldDataDict) -> Self:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        field_value = field_data["value"]

        choices = [t.strip() for t in field_value.get("choices", "").splitlines() if t.strip()]

        if choices:
            initial = [f"c{idx + 1}" for idx, ch in enumerate(choices) if ch[0] == "*"]
            if initial and field_data["type"] in ["dropdown", "radio"]:
                initial = initial[0]
        else:
            initial = field_value.get("initial", "")

        return cls(
            block_id=field_data["id"],
            clean_name=field_value.get("slug", get_field_clean_name(field_value["label"])),
            field_type=field_data["type"],
            label=field_value["label"],
            help_text=field_value["help_text"],
            required=field_value.get("is_required", False),
            default_value=initial,
            disabled=field_value.get("disabled", False),
            choices=[(f"c{idx + 1}", ch.lstrip("*").strip()) for idx, ch in enumerate(choices)],
        )
