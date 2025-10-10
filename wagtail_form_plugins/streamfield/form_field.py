from dataclasses import dataclass
from typing import Any

from .dicts import StreamFieldDataDict

from typing_extensions import Self


@dataclass
class WaftailFormField:
    """
    A dataclass containing field attributes used by wagtail such as in FormMixin.get_data_fields,
    FormBuilder.formfields(), FormBuilder.get_field_options(), and in first attribute of all
    create_field methods.
    """

    clean_name: str
    field_type: str
    label: str
    help_text: str
    required: bool
    choices: dict[str, str]
    default_value: str


@dataclass
class StreamFieldFormField(WaftailFormField):
    """
    A data class representing a field with some extra attributes and syntactic sugar.
    """

    block_id: str
    options: dict[str, Any]
    disabled: bool

    @property
    def slug(self) -> str:
        return self.clean_name

    @property
    def type(self) -> str:
        return self.field_type

    @classmethod
    def from_streamfield_data(cls, field_data: StreamFieldDataDict) -> Self:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        base_options = ["slug", "label", "help_text", "is_required", "initial"]

        field_value = field_data["value"]
        choices = filter(None, [ln.strip() for ln in field_value.get("choices", "").splitlines()])

        return cls(
            block_id=field_data["id"],
            clean_name=field_value["slug"],
            field_type=field_data["type"],
            label=field_value["label"],
            help_text=field_value["help_text"],
            required=field_value["is_required"],
            default_value=field_value.get("initial", ""),
            disabled=field_value["disabled"],
            choices={f"c{idx + 1}": choice for idx, choice in enumerate(choices)},
            options={k: v for k, v in field_value.items() if k not in base_options},
        )
