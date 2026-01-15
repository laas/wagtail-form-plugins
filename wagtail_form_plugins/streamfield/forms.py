"""Form-related classes for the plugins."""

from typing import Any

from django import forms
from django.forms import widgets

from wagtail.contrib.forms.forms import FormBuilder

from .form_field import StreamFieldFormField


class StreamFieldFormBuilder(FormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def create_singleline_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a singleline form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.CharField(widget=widgets.TextInput(attrs=widget_attrs), **options)

    def create_multiline_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a multiline form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.CharField(widget=widgets.Textarea(attrs=widget_attrs), **options)

    def create_date_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DateField:
        """Create a date form field."""

        class DateInput(widgets.DateInput):
            input_type = "date"

        widget_attrs = options.pop("widget_attrs")
        return forms.DateField(widget=DateInput(attrs=widget_attrs), **options)

    def create_time_field(
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.TimeField:
        """Create a time form field."""

        class TimeInput(widgets.TimeInput):
            input_type = "time"

        widget_attrs = options.pop("widget_attrs")
        return forms.TimeField(widget=TimeInput(attrs=widget_attrs), **options)

    def create_datetime_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DateTimeField:
        """Create a datetime form field."""

        class DateTimeInput(widgets.DateTimeInput):
            input_type = "datetime-local"

            def format_value(self, value: str) -> str | None:
                fmt_value = super().format_value(value)
                return fmt_value.rstrip("Z") if fmt_value else None

        widget_attrs = options.pop("widget_attrs")
        return forms.DateTimeField(widget=DateTimeInput(attrs=widget_attrs), **options)

    def create_email_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.EmailField:
        """Create a email form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.EmailField(widget=widgets.EmailInput(attrs=widget_attrs), **options)

    def create_url_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.URLField:
        """Create a url form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.URLField(widget=widgets.URLInput(attrs=widget_attrs), **options)

    def create_number_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.DecimalField:
        """Create a number form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.DecimalField(widget=widgets.NumberInput(attrs=widget_attrs), **options)

    def create_checkbox_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.BooleanField:
        """Create a checkbox form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.BooleanField(widget=widgets.CheckboxInput(attrs=widget_attrs), **options)

    def create_hidden_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.CharField:
        """Create a hidden form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.CharField(widget=widgets.HiddenInput(attrs=widget_attrs), **options)

    def create_dropdown_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.ChoiceField:
        """Create a dropdown form field."""
        widget_attrs = options.pop("widget_attrs")
        return forms.ChoiceField(widget=widgets.Select(attrs=widget_attrs), **options)

    def create_multiselect_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.MultipleChoiceField:
        """Create a multiselect form field."""
        widg_attrs = options.pop("widget_attrs")
        return forms.MultipleChoiceField(widget=widgets.SelectMultiple(attrs=widg_attrs), **options)

    def create_radio_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.ChoiceField:
        """Create a Django choice field with radio widget."""
        widget_attrs = options.pop("widget_attrs")
        return forms.ChoiceField(widget=widgets.RadioSelect(attrs=widget_attrs), **options)

    def create_checkboxes_field(  # ty: ignore invalid-method-override
        self,
        _form_field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> forms.MultipleChoiceField:
        """Create a Django multiple choice field with checkboxes widget."""
        wa = options.pop("widget_attrs")
        if options["required"]:
            wa["required"] = ""
        return forms.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple(attrs=wa), **options)

    def get_field_options(self, form_field: StreamFieldFormField) -> dict[str, Any]:  # ty: ignore invalid-method-override
        """Return the options given to a field. Override to add or modify some options."""
        options = super().get_field_options(form_field)  # label, help_text, required, initial

        if form_field.required:
            options["required"] = True

        if form_field.choices:  # dropdown, multiselect, radio, checkboxes
            options["choices"] = form_field.choices

        options["widget_attrs"] = {
            "data-slug": form_field.slug,
        }

        if form_field.disabled:
            options["widget_attrs"]["readonly"] = ""

        return options
