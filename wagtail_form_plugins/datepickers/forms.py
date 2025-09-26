"""Form-related classes for the Datepicker plugin."""

from datetime import datetime
from typing import Any

from django.forms import widgets

from wagtail_form_plugins.base import BaseFormBuilder
from wagtail_form_plugins.streamfield.forms import DateField, DateTimeField, TimeField


class DateInput(widgets.DateInput):
    """A Django DateInput widget with a date input type."""

    input_type = "date"


class TimeInput(widgets.TimeInput):
    """A Django Time widget with a time input type."""

    input_type = "time"


class DateTimeInput(widgets.DateTimeInput):
    """A Django DateTimeInput widget with a datetime-local input type."""

    input_type = "datetime-local"


class DatePickersFormBuilder(BaseFormBuilder):
    """Form builder class that adds datepicker functionnality to a form."""

    def create_date_field(self, field: Any, options: dict[str, Any]) -> DateField:
        """Create a Django date field."""
        return DateField(**options, widget=DateInput)

    def create_time_field(self, field: Any, options: dict[str, Any]) -> TimeField:
        """Create a Django time field."""
        return TimeField(**options, widget=TimeInput)

    def create_datetime_field(self, field: Any, options: dict[str, Any]) -> DateTimeField:
        """Create a Django datetime field."""
        default = options.get("initial")
        if default:
            default = default.isoformat() if isinstance(default, datetime) else default
            options["initial"] = default.replace("Z", "").split("+")[0]

        return DateTimeField(**options, widget=DateTimeInput)
