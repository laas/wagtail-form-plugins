from django import forms

from wagtail_form_plugins.base.forms import FormBuilderMixin


class DateInput(forms.widgets.DateInput):
    input_type = "date"


class DateTimeInput(forms.widgets.DateTimeInput):
    input_type = "datetime-local"


class DatePickersFormBuilder(FormBuilderMixin):
    def create_date_field(self, field_value, options):
        return forms.DateField(**options, widget=DateInput)

    def create_datetime_field(self, field_value, options):
        return forms.DateTimeField(**options, widget=DateTimeInput)
