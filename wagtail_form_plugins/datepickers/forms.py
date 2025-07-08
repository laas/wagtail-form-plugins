"""Form-related classes for the Datepicker plugin."""

from typing import Any
from django import forms

from wagtail_form_plugins.base.forms import FormBuilderMixin
from wagtail_form_plugins.streamfield.forms import DateField, DateTimeField
from datetime import datetime


class DateInput(forms.widgets.DateInput):
    """A Django DateInput widget with a date input type."""

    input_type = "date"


class DateTimeInput(forms.widgets.DateTimeInput):
    """A Django DateTimeInput widget with a datetime-local input type."""

    input_type = "datetime-local"


class DatePickersFormBuilder(FormBuilderMixin):
    """Form builder mixin that adds datepicker functionnality to a form."""

    def create_date_field(self, field_value: Any, options: dict[str, Any]):
        """Create a Django date field."""
        return DateField(**options, widget=DateInput)

    def create_datetime_field(self, field_value: Any, options: dict[str, Any]):
        """Create a Django datetime field."""
        if "initial" in options:
            default_value = options["initial"]
            if isinstance(default_value, datetime):
                default_value = default_value.isoformat()

            options["initial"] = default_value.replace("Z", "").split("+")[0]

        return DateTimeField(**options, widget=DateTimeInput)
