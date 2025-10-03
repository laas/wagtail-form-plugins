"""Form-related classes for the Streamfield plugin."""

from dataclasses import dataclass

from django import forms
from django.forms import widgets

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.utils import AnyDict

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
class FormField(WaftailFormField):
    """
    A data class representing a field with some extra attributes and syntactic sugar.
    """

    block_id: str
    options: AnyDict
    disabled: bool

    @property
    def slug(self) -> str:
        return self.clean_name

    @property
    def type(self) -> str:
        return self.field_type

    @classmethod
    def from_streamfield_data(cls, field_data: AnyDict) -> Self:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        base_options = ["slug", "label", "help_text", "is_required", "initial"]

        field_value = field_data["value"]
        options = {k: v for k, v in field_value.items() if k not in base_options}
        choice_lines = options.get("choices", "").splitlines()
        choices = filter(None, [line.strip() for line in choice_lines])

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
            options=options,
        )


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

        class DateInput(widgets.DateInput):
            input_type = "date"

        return DateField(**options, widget=DateInput)

    def create_time_field(self, field: FormField, options: AnyDict) -> TimeField:
        """Create a time form field."""

        class TimeInput(widgets.TimeInput):
            input_type = "time"

        return TimeField(**options, widget=TimeInput)

    def create_datetime_field(self, field: FormField, options: AnyDict) -> DateTimeField:
        """Create a datetime form field."""

        class DateTimeInput(widgets.DateTimeInput):
            input_type = "datetime-local"

            def format_value(self, value: str) -> str | None:
                fmt_value = super().format_value(value)
                return fmt_value.rstrip("Z") if fmt_value else None

        return DateTimeField(**options, widget=DateTimeInput)

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
        options = super().get_field_options(field)

        options["slug"] = field.slug

        for k, v in field.options.items():
            if k not in self.extra_field_options:
                options[k] = v

        if "choices" in options:
            options["initial"] = self.get_choices_defaults(options["choices"])
            options["choices"] = self.get_choices_options(options["choices"])

        return options
