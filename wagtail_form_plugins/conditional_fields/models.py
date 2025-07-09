"""Models definition for the Conditional Fields form plugin."""

import json
from datetime import datetime
from typing import Any

from django.forms import Form

from wagtail_form_plugins.base.models import FormMixin
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder

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
    """A mixin used to add conditional fields functionnality to a form."""

    def __init__(self, *args, **kwargs):
        self.form_builder.extra_field_options = ["rule"]
        super().__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        active_fields = []
        if args:
            form.full_clean()
            active_fields = self.get_active_fields(form.cleaned_data)

        fields_raw_data = {fd["value"]["identifier"]: fd for fd in self.form_fields.raw_data}

        for field in form.fields.values():
            raw_data = fields_raw_data[field.identifier]
            if "rule" not in raw_data["value"]:
                continue

            if args and field.identifier not in active_fields:
                field.required = False

            raw_rule = raw_data["value"]["rule"]
            field_rule = self.format_rule(raw_rule[0]) if raw_rule else {}

            new_attributes = {
                "id": raw_data["id"],
                "data-label": field.label,
                "data-widget": field.widget.__class__.__name__,
                "data-rule": json.dumps(field_rule),
            }

            field.widget.attrs.update(new_attributes)

        form.full_clean()
        return form

    @classmethod
    def format_rule(cls, raw_rule: dict[str, Any]):
        """Recusively format a field rule in order to facilitate its parsing on the client side."""
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

    def get_submission_attributes(self, form: Form):
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        attributes = super().get_submission_attributes(form)
        active_fields = self.get_active_fields(form.cleaned_data)
        return {
            **attributes,
            "form_data": {
                k: (v if k in active_fields else None) for k, v in attributes["form_data"].items()
            },
        }

    def get_active_fields(self, form_data: dict[str, Any]):
        """Return the list of fields slug where the computed conditional value of the field is true."""

        def get_choices(field: Any) -> dict[str, str]:
            if "choices" not in field.value:
                return {}

            fmt_choices = StreamFieldFormBuilder.format_field_options(field.value)["choices"]
            return {f"c{ idx + 1 }": choice[0] for idx, choice in enumerate(fmt_choices)}

        slugs = {field.id: field.value["identifier"] for field in self.form_fields}
        choices_slugs = {field.id: get_choices(field) for field in self.form_fields}
        field_types = {field.id: field.block.name for field in self.form_fields}

        def process_rule(rule: dict[str, Any]):
            if rule["field"] in ["and", "or"]:
                results = [process_rule(sub_rule) for sub_rule in rule["rules"]]
                return all(results) if rule["field"] == "and" else any(results)

            a = form_data.get(slugs[rule["field"]])
            field_type = field_types[rule["field"]]

            if field_type in ["singleline", "multiline", "email", "hidden", "url"]:
                b = rule["value_char"]
            elif field_type == "number":
                b = rule["value_number"]
            elif field_type in ["checkboxes", "dropdown", "multiselect", "radio"]:
                b = rule["value_dropdown"]
                if b:
                    b = choices_slugs[rule["field"]][b]

            elif field_type in ["date", "datetime"]:
                b = rule["value_date"]
            else:  # checkbox, file, label
                b = ""

            func = OPERATIONS[rule["operator"]]

            try:
                return func(a, b)
            except Exception:
                print("error when solving rule:", a, rule["operator"], b)
                return False

        active_fields = []
        for field in self.form_fields:
            rules = field.value["rule"]
            if not rules or (
                process_rule(rules[0])
                and (
                    rules[0]["field"] in ["and", "or"] or slugs[rules[0]["field"]] in active_fields
                )
            ):
                active_fields.append(slugs[field.id])

        return active_fields

    class Meta:
        abstract = True
