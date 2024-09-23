import json

from wagtail.contrib.forms.models import FormMixin
from wagtail.contrib.forms.utils import get_field_clean_name


class ConditionalFieldsMixin(FormMixin):
    def __init__(self, *args, **kwargs):
        self.form_builder.extra_field_options = ["rule"]
        super().__init__(*args, **kwargs)

    @classmethod
    def format_rule(cls, raw_rule):
        value = raw_rule["value"]

        if value["field"] in ["and", "or"]:
            return {
                value["field"]: [cls.format_rule(_rule) for _rule in value["rules"]]
            }

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

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)
        form = form_class(*args, **form_params)

        fields_raw_data = {
            get_field_clean_name(fd["value"]["label"]): fd
            for fd in form_params["page"].form_fields.raw_data
        }

        for field in form.fields.values():
            raw_data = fields_raw_data[get_field_clean_name(field.label)]
            rule = raw_data["value"]["rule"]
            field.widget.attrs.update({
                "id": raw_data["id"],
                "class": "form-control",
                "data-rule": json.dumps(self.format_rule(rule[0])) if rule else '{}'
            })

        return form
