import json
from datetime import datetime

from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.base.models import FormMixin

OPERATIONS = {
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
    "is": lambda a, b: a == b,
    "nis": lambda a, b: a != b,
    "lt": lambda a, b: float(a) < float(b),
    "lte": lambda a, b: float(a) <= float(b),
    "ut": lambda a, b: float(a) > float(b),
    "ute": lambda a, b: float(a) >= float(b),
    "bt": lambda a, b: datetime.fromisoformat(a) < datetime.fromisoformat(b),
    "bte": lambda a, b: datetime.fromisoformat(a) <= datetime.fromisoformat(b),
    "at": lambda a, b: datetime.fromisoformat(a) > datetime.fromisoformat(b),
    "ate": lambda a, b: datetime.fromisoformat(a) >= datetime.fromisoformat(b),
    "ct": lambda a, b: b in a,
    "nct": lambda a, b: b not in a,
    "c": lambda a, b: a,
    "nc": lambda a, b: not a,
}


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

    @classmethod
    def solve_rules(cls, fields_data, form_fields):
        slugs = {field.id: get_field_clean_name(field.value["label"]) for field in form_fields}

        to_hide = []
        for field in form_fields:
            for rule in field.value["rule"]:
                a = fields_data[slugs[rule["field"]]][1]
                b = (
                    rule["value_char"]
                    or rule["value_number"]
                    or rule["value_dropdown"]
                    or rule["value_date"]
                    or ""
                )
                func = OPERATIONS[rule["operator"]]

                # print("solving rule:", field.value["label"], a, rule["operator"], b)
                try:
                    should_show = func(a, b)
                except Exception:
                    print("error when solving rule:", a, rule["operator"], b)
                    should_show = False

                if not should_show:
                    to_hide.append(slugs[field.id])

        return {fd_slug: fd for fd_slug, fd in fields_data.items() if fd_slug not in to_hide}

    class Meta:
        abstract = True
