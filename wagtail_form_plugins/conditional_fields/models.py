import json

from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.base.models import FormMixin


class ConditionalFieldsFormMixin(FormMixin):
    def __init__(self, *args, **kwargs):
        self.form_builder.extra_field_options = ["rule"]
        super().__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        fields_raw_data = {
            get_field_clean_name(fd["value"]["label"]): fd for fd in form.page.form_fields.raw_data
        }

        for field in form.fields.values():
            raw_data = fields_raw_data[get_field_clean_name(field.label)]
            if "rule" not in raw_data["value"]:
                continue
            raw_rule = raw_data["value"]["rule"]

            new_attributes = {
                "id": raw_data["id"],
                # "class": "form-control", # boostrap forms
                "data-label": field.label,
                "data-widget": field.widget.__class__.__name__,
                "data-rule": json.dumps(self.format_rule(raw_rule[0])) if raw_rule else "{}",
            }

            field.widget.attrs.update(new_attributes)

        return form

    @classmethod
    def format_rule(cls, raw_rule):
        value = raw_rule["value"]

        if value["field"] in ["and", "or"]:
            return {value["field"]: [cls.format_rule(_rule) for _rule in value["rules"]]}

        return {
            "entry": {
                "target": value["field"],
                "val": value["value_date"]
                or value["value_dropdown"]
                or value["value_number"]
                or value["value_char"],
                "opr": value["operator"],
            }
        }

    class Meta:
        abstract = True
