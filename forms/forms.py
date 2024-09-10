from collections import OrderedDict

from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name


class StreamFieldFormBuilder(FormBuilder):
    def create_dropdown_field(self, field_value, options):
        options["choices"] = self.get_formatted_field_choices(field_value)
        options["initial"] = self.get_formatted_field_initial(field_value)[0]
        return super().create_dropdown_field(field_value, options)

    def create_multiselect_field(self, field_value, options):
        options["choices"] = self.get_formatted_field_choices(field_value)
        options["initial"] = self.get_formatted_field_initial(field_value)
        return super().create_multiselect_field(field_value, options)

    def create_radio_field(self, field_value, options):
        options["choices"] = self.get_formatted_field_choices(field_value)
        options["initial"] = self.get_formatted_field_initial(field_value)[0]
        return super().create_radio_field(field_value, options)

    def create_checkboxes_field(self, field_value, options):
        options["choices"] = self.get_formatted_field_choices(field_value)
        options["initial"] = self.get_formatted_field_initial(field_value)
        return super().create_checkboxes_field(field_value, options)

    def get_formatted_field_choices(self, field_data):
        return [
            (
                get_field_clean_name(choice["value"]["label"].strip()),
                choice["value"]["label"],
            )
            for choice in field_data["choices"]
        ]

    def get_formatted_field_initial(self, field_data):
        return [
            choice["value"]["label"]
            for choice in field_data["choices"]
            if choice["value"]["initial"]
        ]

    @property
    def formfields(self):
        formfields = OrderedDict()

        for field_data in self.fields.raw_data:
            options = self.get_field_options(field_data)
            create_field = self.get_create_field_function(field_data["type"])
            clean_name = get_field_clean_name(field_data["value"]["label"])
            formfields[clean_name] = create_field(field_data["value"], options)

        return formfields

    def get_field_options(self, field_data):
        options = {**field_data["value"]}
        if not getattr(settings, "WAGTAILFORMS_HELP_TEXT_ALLOW_HTML", False):
            options["help_text"] = conditional_escape(options["help_text"])
        return options
