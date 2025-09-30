"""Form-related classes for the Streamfield plugin."""

from dataclasses import dataclass

from django import forms

from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.forms import FormBuilder

from wagtail_form_plugins.utils import AnyDict


@dataclass
class FormField:
    """
    The field class used in the form.
    It defines all required attributes used by wagtail such as in FormMixin.get_data_fields,
    FormBuilder.formfields(), FormBuilder.get_field_options(), and in first attribute of all
    create_field methods, as well as its streamfield block id and an options dict to add more field
    attributes via plugins.
    """

    clean_name: str
    field_type: str
    label: str
    help_text: str
    required: bool
    default_value: str

    block_id: str
    options: AnyDict


class FieldWithSlug:
    """A mixin used to add a slug attribute to Django Field classes."""

    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop("slug")
        super().__init__(*args, **kwargs)


class CharField(FieldWithSlug, forms.CharField):
    """A Django CharField class with an addititional slug attribute."""

    pass


class DateField(FieldWithSlug, forms.DateField):
    """A Django DateField class with an addititional slug attribute."""

    pass


class TimeField(FieldWithSlug, forms.TimeField):
    """A Django TimeField class with an addititional slug attribute."""

    pass


class DateTimeField(FieldWithSlug, forms.DateTimeField):
    """A Django DateTimeField class with an addititional slug attribute."""

    pass


class EmailField(FieldWithSlug, forms.EmailField):
    """A Django EmailField class with an addititional slug attribute."""

    pass


class URLField(FieldWithSlug, forms.URLField):
    """A Django URLField class with an addititional slug attribute."""

    pass


class DecimalField(FieldWithSlug, forms.DecimalField):
    """A Django DecimalField class with an addititional slug attribute."""

    pass


class BooleanField(FieldWithSlug, forms.BooleanField):
    """A Django BooleanField class with an addititional slug attribute."""

    pass


class ChoiceField(FieldWithSlug, forms.ChoiceField):
    """A Django ChoiceField class with an addititional slug attribute."""

    pass


class MultipleChoiceField(FieldWithSlug, forms.MultipleChoiceField):
    """A Django MultipleChoiceField class with an addititional slug attribute."""

    pass


class StreamFieldFormBuilder(FormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def __init__(self, fields: list[FormField]):
        super().__init__(fields)
        self.extra_field_options = []

    def create_singleline_field(self, field: FormField, options: AnyDict) -> CharField:
        """Create a singleline form field."""
        return CharField(**options)

    def create_multiline_field(self, field: FormField, options: AnyDict) -> CharField:
        """Create a multiline form field."""
        options.setdefault("widget", forms.Textarea)
        return CharField(**options)

    def create_date_field(self, field: FormField, options: AnyDict) -> DateField:
        """Create a date form field."""
        return DateField(**options)

    def create_time_field(self, field: FormField, options: AnyDict) -> TimeField:
        """Create a time form field."""
        return TimeField(**options)

    def create_datetime_field(self, field: FormField, options: AnyDict) -> DateTimeField:
        """Create a datetime form field."""
        return DateTimeField(**options)

    def create_email_field(self, field: FormField, options: AnyDict) -> EmailField:
        """Create a email form field."""
        return EmailField(**options)

    def create_url_field(self, field: FormField, options: AnyDict) -> URLField:  # type: ignore
        """Create a url form field."""
        return URLField(**options)

    def create_number_field(self, field: FormField, options: AnyDict) -> DecimalField:
        """Create a number form field."""
        return DecimalField(**options)

    def create_checkbox_field(self, field: FormField, options: AnyDict) -> BooleanField:
        """Create a checkbox form field."""
        return BooleanField(**options)

    def create_hidden_field(self, field: FormField, options: AnyDict) -> CharField:
        """Create a hidden form field."""
        options.setdefault("widget", forms.HiddenInput)
        return CharField(**options)

    def create_dropdown_field(self, field: FormField, options: AnyDict) -> ChoiceField:
        """Create a dropdown form field."""
        return ChoiceField(**options)

    def create_multiselect_field(self, field: FormField, options: AnyDict) -> MultipleChoiceField:
        """Create a multiselect form field."""
        return MultipleChoiceField(**options)

    def create_radio_field(self, field: FormField, options: AnyDict) -> ChoiceField:
        """Create a Django choice field with radio widget."""
        return ChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(self, field: FormField, options: AnyDict) -> MultipleChoiceField:
        """Create a Django multiple choice field with checkboxes widget."""
        return MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **options)

    @classmethod
    def get_choices_defaults(cls, str_choices: str) -> list[str]:
        """Return formatted choices of choice-based fields."""
        return [
            choice.strip()
            for choice in str_choices.split("\n")
            if choice and choice.startswith("*")
        ]

    @classmethod
    def get_choices_options(cls, str_choices: str) -> list[tuple[str, str]]:
        """Return formatted initial options of choice-based fields."""
        return [
            (get_field_clean_name(ch.lstrip("*")), ch.lstrip("*").strip())
            for ch in str_choices.split("\n")
            if ch
        ]

    def get_field_options(self, field: FormField) -> AnyDict:
        """Return the options given to a field. Override to add or modify some options."""
        options = {
            **super().get_field_options(field),
            "slug": field.clean_name,
            **{k: v for k, v in field.options.items() if k not in self.extra_field_options},
        }

        if "choices" in options:
            options["initial"] = self.get_choices_defaults(options["choices"])
            options["choices"] = self.get_choices_options(options["choices"])

        return options
