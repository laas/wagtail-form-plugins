"""Form-related classes for the plugins."""

from typing import Any

from django import forms
from django.forms import widgets

from wagtail.contrib.forms.forms import FormBuilder

from .form_field import StreamFieldFormField


class StreamFieldFormBuilder(FormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def __init__(self, fields: list[StreamFieldFormField]):
        super().__init__(fields)
        self.extra_field_options = []

    def create_singleline_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a singleline form field."""
        widget = widgets.TextInput(attrs={"slug": form_field.slug})
        return forms.CharField(widget=widget, **options)

    def create_multiline_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a multiline form field."""
        widget = widgets.Textarea(attrs={"slug": form_field.slug})
        return forms.CharField(widget=widget, **options)

    def create_date_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DateField:
        """Create a date form field."""

        class DateInput(widgets.DateInput):
            input_type = "date"

        widget = DateInput(attrs={"slug": form_field.slug})
        return forms.DateField(widget=widget, **options)

    def create_time_field(
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.TimeField:
        """Create a time form field."""

        class TimeInput(widgets.TimeInput):
            input_type = "time"

        widget = TimeInput(attrs={"slug": form_field.slug})
        return forms.TimeField(widget=widget, **options)

    def create_datetime_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DateTimeField:
        """Create a datetime form field."""

        class DateTimeInput(widgets.DateTimeInput):
            input_type = "datetime-local"

            def format_value(self, value: str) -> str | None:
                fmt_value = super().format_value(value)
                return fmt_value.rstrip("Z") if fmt_value else None

        widget = DateTimeInput(attrs={"slug": form_field.slug})
        return forms.DateTimeField(widget=widget, **options)

    def create_email_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.EmailField:
        """Create a email form field."""
        widget = widgets.EmailInput(attrs={"slug": form_field.slug})
        return forms.EmailField(widget=widget, **options)

    def create_url_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.URLField:
        """Create a url form field."""
        widget = widgets.URLInput(attrs={"slug": form_field.slug})
        return forms.URLField(widget=widget, **options)

    def create_number_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DecimalField:
        """Create a number form field."""
        widget = widgets.NumberInput(attrs={"slug": form_field.slug})
        return forms.DecimalField(widget=widget, **options)

    def create_checkbox_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.BooleanField:
        """Create a checkbox form field."""
        widget = widgets.CheckboxInput(attrs={"slug": form_field.slug})
        return forms.BooleanField(widget=widget, **options)

    def create_hidden_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a hidden form field."""
        widget = widgets.HiddenInput(attrs={"slug": form_field.slug})
        return forms.CharField(widget=widget, **options)

    def create_dropdown_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.ChoiceField:
        """Create a dropdown form field."""
        widget = widgets.Select(attrs={"slug": form_field.slug})
        return forms.ChoiceField(widget=widget, **options)

    def create_multiselect_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.MultipleChoiceField:
        """Create a multiselect form field."""
        widget = widgets.SelectMultiple(attrs={"slug": form_field.slug})
        return forms.MultipleChoiceField(widget=widget, **options)

    def create_radio_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.ChoiceField:
        """Create a Django choice field with radio widget."""
        widget = widgets.RadioSelect(attrs={"slug": form_field.slug})
        return forms.ChoiceField(widget=widget, **options)

    def create_checkboxes_field(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.MultipleChoiceField:
        """Create a Django multiple choice field with checkboxes widget."""
        widget = widgets.CheckboxSelectMultiple(attrs={"slug": form_field.slug})
        return forms.MultipleChoiceField(widget=widget, **options)

    def get_field_options(self, form_field: StreamFieldFormField) -> dict[str, Any]:  # type: ignore[reportIncompatibleMethodOverride]
        """Return the options given to a field. Override to add or modify some options."""
        options = super().get_field_options(form_field)  # label, help_text, required, initial

        options["disabled"] = form_field.disabled
        if form_field.choices:  # dropdown, multiselect, radio, checkboxes
            options["choices"] = form_field.choices

        for k, v in form_field.options.items():
            if k not in self.extra_field_options:
                options[k] = v

        return options
