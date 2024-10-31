from django import forms

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_mixins.base.models import FormMixin


class Field:
    label: str
    help_text: str
    required: bool
    default_value: str
    field_type: str
    clean_name: str
    options: dict

    @staticmethod
    def from_streamfield_data(field_data):
        field_value = field_data["value"]
        base_options = ["label", "help_text", "initial"]

        field = Field()
        field.label = field_value["label"]
        field.clean_name = get_field_clean_name(field.label)
        field.help_text = field_value["help_text"]
        field.required = field_value["required"]
        field.default_value = field_value.get("initial", None)
        field.field_type = field_data["type"]
        field.options = {k: v for k, v in field_value.items() if k not in base_options}
        return field


class StreamFieldFormBuilder(FormBuilder):
    extra_field_options = []

    def create_dropdown_field(self, field, options):
        return forms.ChoiceField(**options)

    def create_multiselect_field(self, field, options):
        return forms.MultipleChoiceField(**options)

    def create_radio_field(self, field, options):
        return forms.ChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(self, field, options):
        return forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, **options)

    def format_field_options(self, options: dict):
        formatted_choices = []
        formatted_initial = []

        if "choices" not in options:
            return options

        for choice in options["choices"]:
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

    def get_field_options(self, field: Field):
        extra_options = self.extra_field_options if hasattr(self, "extra_field_options") else []
        options = {
            **super().get_field_options(field),
            **{k: v for k, v in field.options.items() if k not in extra_options},
        }
        return self.format_field_options(options)


class StreamFieldFormMixin(FormMixin):
    form_builder = StreamFieldFormBuilder

    def get_form_fields(self):
        return [Field.from_streamfield_data(field_data) for field_data in self.form_fields.raw_data]

    class Meta:
        abstract = True
