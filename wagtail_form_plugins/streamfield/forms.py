"""Form-related classes for the Streamfield plugin."""

from typing import Any

from django import forms

from wagtail.compat import URLField as WagtailURLField
from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.base import BaseField, BaseFormBuilder


class FieldWithId:
    """A mixin used to add a slug attribute to Django Field classes."""

    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop("slug")
        super().__init__(*args, **kwargs)


class CharField(FieldWithId, forms.CharField):
    """A Django CharField class with an addititional slug attribute."""

    pass


class DateField(FieldWithId, forms.DateField):
    """A Django DateField class with an addititional slug attribute."""

    pass


class TimeField(FieldWithId, forms.TimeField):
    """A Django TimeField class with an addititional slug attribute."""

    pass


class DateTimeField(FieldWithId, forms.DateTimeField):
    """A Django DateTimeField class with an addititional slug attribute."""

    pass


class EmailField(FieldWithId, forms.EmailField):
    """A Django EmailField class with an addititional slug attribute."""

    pass


class URLField(FieldWithId, WagtailURLField):
    """A Django URLField class with an addititional slug attribute."""

    pass


class DecimalField(FieldWithId, forms.DecimalField):
    """A Django DecimalField class with an addititional slug attribute."""

    pass


class BooleanField(FieldWithId, forms.BooleanField):
    """A Django BooleanField class with an addititional slug attribute."""

    pass


class ChoiceField(FieldWithId, forms.ChoiceField):
    """A Django ChoiceField class with an addititional slug attribute."""

    pass


class MultipleChoiceField(FieldWithId, forms.MultipleChoiceField):
    """A Django MultipleChoiceField class with an addititional slug attribute."""

    pass


class StreamFieldFormBuilder(BaseFormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def create_singleline_field(self, field: BaseField, options: dict[str, Any]) -> CharField:
        """Create a singleline form field."""
        return CharField(**options)

    def create_multiline_field(self, field: BaseField, options: dict[str, Any]) -> CharField:
        """Create a multiline form field."""
        options.setdefault("widget", forms.Textarea)
        return CharField(**options)

    def create_date_field(self, field: BaseField, options: dict[str, Any]) -> DateField:
        """Create a date form field."""
        return DateField(**options)

    def create_time_field(self, field: BaseField, options: dict[str, Any]) -> TimeField:
        """Create a time form field."""
        return TimeField(**options)

    def create_datetime_field(self, field: BaseField, options: dict[str, Any]) -> DateTimeField:
        """Create a datetime form field."""
        return DateTimeField(**options)

    def create_email_field(self, field: BaseField, options: dict[str, Any]) -> EmailField:
        """Create a email form field."""
        return EmailField(**options)

    def create_url_field(self, field: BaseField, options: dict[str, Any]) -> URLField:
        """Create a url form field."""
        return URLField(**options)

    def create_number_field(self, field: BaseField, options: dict[str, Any]) -> DecimalField:
        """Create a number form field."""
        return DecimalField(**options)

    def create_checkbox_field(self, field: BaseField, options: dict[str, Any]) -> BooleanField:
        """Create a checkbox form field."""
        return BooleanField(**options)

    def create_hidden_field(self, field: BaseField, options: dict[str, Any]) -> CharField:
        """Create a hidden form field."""
        options.setdefault("widget", forms.HiddenInput)
        return CharField(**options)

    def create_dropdown_field(self, field: BaseField, options: dict[str, Any]) -> ChoiceField:
        """Create a dropdown form field."""
        return ChoiceField(**options)

    def create_multiselect_field(
        self,
        field: BaseField,
        options: dict[str, Any],
    ) -> MultipleChoiceField:
        """Create a multiselect form field."""
        return MultipleChoiceField(**options)

    def create_radio_field(self, field: BaseField, options: dict[str, Any]) -> ChoiceField:
        """Create a Django choice field with radio widget."""
        return ChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(
        self,
        field: BaseField,
        options: dict[str, Any],
    ) -> MultipleChoiceField:
        """Create a Django multiple choice field with checkboxes widget."""
        return MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **options)

    @staticmethod
    def format_field_options(options: dict) -> dict[str, Any]:
        """Add formatted field choices and initial options of choice-based fields."""
        formatted_choices = []
        formatted_initial = []

        if "choices" not in options:
            return options

        for choice in [ch.strip() for ch in options["choices"].split("\n") if ch]:
            is_initial = choice.startswith("*")
            label = choice[1:] if is_initial else choice
            slug = get_field_clean_name(label)
            formatted_choices.append((slug, label))

            if is_initial:
                formatted_initial.append(slug)

        return {
            **options,
            "choices": formatted_choices,
            "initial": formatted_initial,
        }

    def get_field_options(self, field: BaseField) -> dict[str, Any]:
        """Return the options given to a field. Override to add or modify some options."""
        options = {
            **super().get_field_options(field),
            "slug": field.clean_name,
            **{
                k: v
                for k, v in field.options.items()
                if k not in self.get_all_extra_field_options()
            },
        }

        # options = {"label": field.label}
        # if getattr(settings, "WAGTAILFORMS_HELP_TEXT_ALLOW_HTML", False):
        #     options["help_text"] = field.help_text
        # else:
        #     options["help_text"] = conditional_escape(field.help_text)
        # options["required"] = field.required
        # options["initial"] = field.default_value
        return self.format_field_options(options)
