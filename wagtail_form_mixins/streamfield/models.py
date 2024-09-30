from collections import OrderedDict

from django import forms
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import FormMixin
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name


class StreamFieldFormBuilder(FormBuilder):
    extra_field_options = []

    def create_dropdown_field(self, field_value, options):
        _options = self.format_field_options(options, field_value["choices"])
        return forms.ChoiceField(**_options)

    def create_multiselect_field(self, field_value, options):
        _options = self.format_field_options(options, field_value["choices"])
        return forms.MultipleChoiceField(**_options)

    def create_radio_field(self, field_value, options):
        _options = self.format_field_options(options, field_value["choices"])
        return forms.ChoiceField(widget=forms.RadioSelect, **_options)

    def create_checkboxes_field(self, field_value, options):
        _options = self.format_field_options(options, field_value["choices"])
        return forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **_options)

    def format_field_options(self, options, choices):
        formatted_choices = []
        formatted_initial = []

        for choice in choices:
            label = choice["value"]["label"].strip()
            slug = get_field_clean_name(label)
            formatted_choices.append((slug, label))
            if choice["value"]["initial"]:
                formatted_initial.append(slug)

        return {
            **options,
            "choices": formatted_choices,
            "initial": formatted_initial,
        }

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

        if hasattr(self, "extra_field_options"):
            for option in self.extra_field_options:
                if option in options:
                    options.pop(option)

        return options


class StreamFieldFormMixin(FormMixin):
    form_builder = StreamFieldFormBuilder

    def get_form_fields(self):
        return self.form_fields

    def get_data_fields(self):
        data_fields = [
            ("submit_time", _("Submission date")),
        ]

        data_fields += [
            (get_field_clean_name(data["value"]["label"]), data["value"]["label"])
            for data in self.get_form_fields().raw_data
        ]

        return data_fields
