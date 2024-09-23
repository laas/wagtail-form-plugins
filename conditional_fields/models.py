import json

from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import FormMixin
from wagtail.contrib.forms.utils import get_field_clean_name


class ConditionalFieldsMixin(FormMixin):
    def __init__(self, *args, **kwargs):
        self.form_builder.extra_field_options = ["rule"]
        super().__init__(*args, **kwargs)

    @classmethod
    def format_rule(cls, fields_id, rule):
        conditions = []
        for rule_entry in rule:
            if rule_entry["type"] in ("bool_and", "bool_or"):
                rule_block = cls.format_rule(fields_id, rule_entry["value"])
                conditions.append({rule_entry["type"][5:]: rule_block})
            else:
                rule_entry["value"]["field_id"] = fields_id[rule_entry["value"]["field_id"]]
                conditions.append(rule_entry["value"])

        return [{}] if not conditions else conditions

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)
        form = form_class(*args, **form_params)

        # --- WIP ---

        raw_data = form_params["page"].form_fields.raw_data
        fields_data = {
            get_field_clean_name(fd["value"]["label"]): fd for fd in raw_data
        }

        dom_ids = {fields_data[id]["id"]: f"id_{id}" for id in form.fields.keys()}

        for name, field in form.fields.items():
            raw_rule = fields_data[name]["value"]["rule"]
            rule = self.format_rule(dom_ids, raw_rule)[0]
            field.widget.attrs.update(
                {
                    "data-rule": json.dumps(rule),
                    "class": "form-control",
                }
            )

        return form
