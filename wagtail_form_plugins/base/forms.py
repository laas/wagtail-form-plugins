"""Base classes for form builder mixins."""

from dataclasses import dataclass
from typing import Any, ClassVar

from wagtail.contrib.forms.forms import FormBuilder


@dataclass
class BaseField:
    """
    The field class used in the form streamfield.
    It is used by wagtail, such as FormMixin.get_data_fields, FormBuilder.formfields() and
    FormBuilder.get_field_options(), and in first attribute of all create_field methods.
    Required attributes: clean_name, field_type, label, help_text, required, default_value
    """

    clean_name: str
    field_type: str
    label: str
    help_text: str
    required: bool
    default_value: str

    id: str
    options: dict[str, Any]


class BaseFormBuilder(FormBuilder):
    """Base class for form builder classes."""

    subclasses: ClassVar = []
    extra_field_options: ClassVar[list[str]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @classmethod
    def get_all_extra_field_options(cls) -> list[str]:
        """Get all the extra field options from all subclasses."""
        extra_field_options = []
        for subclass in cls.subclasses:
            if hasattr(subclass, "extra_field_options"):
                extra_field_options += subclass.extra_field_options

        return extra_field_options
