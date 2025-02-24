"""Form-related classes for the Streamfield plugin."""

from typing import Any
from django import forms

from wagtail_form_plugins.base.forms import FormBuilderMixin
from wagtail.contrib.forms.utils import get_field_clean_name


class Field:
    """The field class used in the form streamfield."""

    label: str
    help_text: str
    required: bool
    default_value: str
    field_type: str
    clean_name: str
    options: dict

    @staticmethod
    def from_streamfield_data(field_data: dict[str, Any]):
        """Create and return a field based on field data."""
        field_value = field_data["value"]
        base_options = ["label", "help_text", "initial"]

        field = Field()
        field.label = field_value["label"]
        field.clean_name = get_field_clean_name(field.label)
        field.help_text = field_value["help_text"]
        field.required = field_value["required"]
        field.default_value = field_value.get("initial", None)
        field.field_type = field_data["type"]
        field.options = {k: v for k, v in field_value.items() if k not in base_options}
        return field


class StreamFieldFormBuilder(FormBuilderMixin):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def create_dropdown_field(self, field: Any, options: dict[str, Any]):
        """Create a Django choice field."""
        return forms.ChoiceField(**options)

    def create_multiselect_field(self, field: Any, options: dict[str, Any]):
        """Create a Django multiple choice field."""
        return forms.MultipleChoiceField(**options)

    def create_radio_field(self, field: Any, options: dict[str, Any]):
        """Create a Django choice field with radio widget."""
        return forms.ChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(self, field: Any, options: dict[str, Any]):
        """Create a Django multiple choice field with checkboxes widget."""
        return forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **options)

    def format_field_options(self, options: dict):
        """Add formatted field choices and initial options of choice-based fields."""
        formatted_choices = []
        formatted_initial = []

        if "choices" not in options:
            return options

        for choice in options["choices"]:
            label = choice["value"]["label"].strip()
            slug = get_field_clean_name(label)
            formatted_choices.append((slug, label))
            if choice["value"]["initial"]:
                formatted_initial.append(slug)

        return {
            **options,
            "choices": formatted_choices,
            "initial": formatted_initial,
        }

    def get_field_options(self, field: Field):
        """Return the options given to a field. Override to add or modify some options."""
        options = {
            **super().get_field_options(field),
            **{k: v for k, v in field.options.items() if k not in self.get_extra_field_options()},
        }
        return self.format_field_options(options)
