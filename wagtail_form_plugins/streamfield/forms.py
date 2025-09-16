"""Form-related classes for the Streamfield plugin."""

from typing import Any

from django import forms
from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.base.forms import FormBuilderMixin


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
        field.clean_name = field_value["identifier"]
        field.help_text = field_value["help_text"]
        field.required = field_value["required"]
        field.default_value = field_value.get("initial", None)
        field.field_type = field_data["type"]
        field.options = {k: v for k, v in field_value.items() if k not in base_options}
        return field


class FieldWithIdMixin:
    """A mixin used to add an identifier attribute to Django Field classes."""

    def __init__(self, *args, **kwargs):
        self.identifier = kwargs.pop("identifier")
        super().__init__(*args, **kwargs)


class CharField(FieldWithIdMixin, forms.CharField):
    """A Django CharField class with an addititional identifier attribute."""

    pass


class DateField(FieldWithIdMixin, forms.DateField):
    """A Django DateField class with an addititional identifier attribute."""

    pass


class TimeField(FieldWithIdMixin, forms.TimeField):
    """A Django TimeField class with an addititional identifier attribute."""

    pass


class DateTimeField(FieldWithIdMixin, forms.DateTimeField):
    """A Django DateTimeField class with an addititional identifier attribute."""

    pass


class EmailField(FieldWithIdMixin, forms.EmailField):
    """A Django EmailField class with an addititional identifier attribute."""

    pass


class URLField(FieldWithIdMixin, forms.URLField):
    """A Django URLField class with an addititional identifier attribute."""

    pass


class DecimalField(FieldWithIdMixin, forms.DecimalField):
    """A Django DecimalField class with an addititional identifier attribute."""

    pass


class BooleanField(FieldWithIdMixin, forms.BooleanField):
    """A Django BooleanField class with an addititional identifier attribute."""

    pass


class ChoiceField(FieldWithIdMixin, forms.ChoiceField):
    """A Django ChoiceField class with an addititional identifier attribute."""

    pass


class MultipleChoiceField(FieldWithIdMixin, forms.MultipleChoiceField):
    """A Django MultipleChoiceField class with an addititional identifier attribute."""

    pass


class StreamFieldFormBuilder(FormBuilderMixin):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def create_singleline_field(self, field: Field, options: dict[str, Any]):
        """Create a singleline form field."""
        return CharField(**options)

    def create_multiline_field(self, field: Field, options: dict[str, Any]):
        """Create a multiline form field."""
        options.setdefault("widget", forms.Textarea)
        return CharField(**options)

    def create_date_field(self, field: Field, options: dict[str, Any]):
        """Create a date form field."""
        return DateField(**options)

    def create_time_field(self, field: Field, options: dict[str, Any]):
        """Create a time form field."""
        return TimeField(**options)

    def create_datetime_field(self, field: Field, options: dict[str, Any]):
        """Create a datetime form field."""
        return DateTimeField(**options)

    def create_email_field(self, field: Field, options: dict[str, Any]):
        """Create a email form field."""
        return EmailField(**options)

    def create_url_field(self, field: Field, options: dict[str, Any]):
        """Create a url form field."""
        return URLField(**options)

    def create_number_field(self, field: Field, options: dict[str, Any]):
        """Create a number form field."""
        return DecimalField(**options)

    def create_checkbox_field(self, field: Field, options: dict[str, Any]):
        """Create a checkbox form field."""
        return BooleanField(**options)

    def create_hidden_field(self, field: Field, options: dict[str, Any]):
        """Create a hidden form field."""
        options.setdefault("widget", forms.HiddenInput)
        return CharField(**options)

    def create_dropdown_field(self, field: Field, options: dict[str, Any]):
        """Create a dropdown form field."""
        return ChoiceField(**options)

    def create_multiselect_field(self, field: Field, options: dict[str, Any]):
        """Create a multiselect form field."""
        return MultipleChoiceField(**options)

    def create_radio_field(self, field: Field, options: dict[str, Any]):
        """Create a Django choice field with radio widget."""
        return ChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(self, field: Field, options: dict[str, Any]):
        """Create a Django multiple choice field with checkboxes widget."""
        return MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **options)

    @staticmethod
    def format_field_options(options: dict):
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

    def get_field_options(self, field: Field):
        """Return the options given to a field. Override to add or modify some options."""
        options = {
            **super().get_field_options(field),
            **{k: v for k, v in field.options.items() if k not in self.get_extra_field_options()},
        }
        return self.format_field_options(options)
