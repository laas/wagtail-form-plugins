"""Models definition for the Conditional Fields form plugin."""

import json
from datetime import date
from datetime import datetime as dt
from datetime import timezone as tz
from typing import Any

from django.forms import BaseForm, Field, Form

from wagtail_form_plugins.base import BaseFormPage
from wagtail_form_plugins.base.forms import BaseField
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder

OPERATIONS = {
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
    "is": lambda a, b: a == b,
    "nis": lambda a, b: a != b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "ut": lambda a, b: a > b,
    "ute": lambda a, b: a >= b,
    "bt": lambda a, b: a < b,
    "bte": lambda a, b: a <= b,
    "at": lambda a, b: a > b,
    "ate": lambda a, b: a >= b,
    "ct": lambda a, b: b in a,
    "nct": lambda a, b: b not in a,
    "c": lambda a, b: a,
    "nc": lambda a, b: not a,
}

StrDict = dict[str, str]
AnyDict = dict[str, Any]


class FormField(Field):
    slug: str
    id: str


class ConditionalFieldsFormPage(BaseFormPage):
    """Form page used to add conditional fields functionnality to a form."""

    def __init__(self, *args, **kwargs):
        self.form_builder_class.extra_field_options = ["rule"]
        super().__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        active_fields = []
        if args:
            form.full_clean()
            active_fields = self.get_active_fields(form.cleaned_data)

        for form_field in form.fields.values():  # type: ignore
            form_field: FormField
            field = self.get_form_fields_dict()[form_field.slug]

            if "rule" not in field.options:
                continue

            if args and form_field.slug not in active_fields:  # type: ignore
                form_field.required = False

            raw_rule = field.options["rule"]
            field_rule = self.format_rule(raw_rule[0]) if raw_rule else {}

            new_attributes = {
                "id": field.id,
                "data-label": form_field.label,
                "data-widget": form_field.widget.__class__.__name__,
                "data-rule": json.dumps(field_rule),
            }

            form_field.widget.attrs.update(new_attributes)

        form.full_clean()
        return form

    @classmethod
    def format_value_date(cls, value: Any) -> int:
        fmt_value = value or dt.now()
        if isinstance(fmt_value, str):
            fmt_value = dt.strptime(fmt_value, "%Y-%m-%d").replace(tzinfo=tz.utc)
        elif isinstance(fmt_value, date):
            fmt_value = dt.combine(fmt_value, dt.min.time())
        return int(fmt_value.timestamp())

    @classmethod
    def format_value_time(cls, value: Any) -> int:
        fmt_value = value or dt.now()
        if isinstance(fmt_value, str):
            fmt_value = dt.fromisoformat(f"1970-01-01T{fmt_value}")
        return int(fmt_value.timestamp())

    @classmethod
    def format_value_datetime(cls, value: Any) -> int:
        fmt_value = value or dt.now()
        if isinstance(fmt_value, str):
            fmt_value = dt.fromisoformat(fmt_value)
        return int(fmt_value.timestamp())

    @classmethod
    def format_rule(cls, raw_rule: dict[str, Any]) -> dict[str, Any]:
        """Recusively format a field rule in order to facilitate its parsing on the client side."""
        value = raw_rule["value"]

        if value["field"] in ["and", "or"]:
            return {value["field"]: [cls.format_rule(_rule) for _rule in value["rules"]]}

        if value.get("value_date"):
            fmt_value = cls.format_value_date(value["value_date"])
        elif value.get("value_time"):
            fmt_value = cls.format_value_time(value["value_time"])
        elif value.get("value_datetime"):
            fmt_value = cls.format_value_time(value["value_datetime"])
        elif value.get("value_dropdown"):
            fmt_value = value["value_dropdown"]
        elif value.get("value_number"):
            fmt_value = int(value["value_number"])
        else:
            fmt_value = value["value_char"]

        return {
            "entry": {
                "target": value["field"],
                "val": fmt_value,
                "opr": value["operator"],
            },
        }

    def get_submission_attributes(self, form: Form) -> dict[str, Any]:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        attributes = super().get_submission_attributes(form)
        active_fields = self.get_active_fields(form.cleaned_data)
        return {
            **attributes,
            "form_data": {
                k: (v if k in active_fields else None) for k, v in attributes["form_data"].items()
            },
        }

    def process_rule(
        self,
        form_data: AnyDict,
        choices_slugs: dict[str, StrDict],
        rule: AnyDict,
    ) -> Any:
        field_id = str(rule.get("field", ""))
        field = self.get_form_fields_dict()[field_id]

        if field_id in ["and", "or"]:
            results = [
                self.process_rule(form_data, choices_slugs, sub_rule) for sub_rule in rule["rules"]
            ]
            return all(results) if field_id == "and" else any(results)

        left_operand = form_data.get(field.clean_name)

        if field.field_type in ["singleline", "multiline", "email", "hidden", "url"]:
            right_operand = rule["value_char"]
        elif field.field_type == "number":
            right_operand = float(rule["value_number"])
        elif field.field_type in ["checkboxes", "dropdown", "multiselect", "radio"]:
            choice = choices_slugs.get(field_id)
            dropdown_val: str = rule["value_dropdown"]
            right_operand = choice[dropdown_val] if dropdown_val and choice else dropdown_val

        elif field.field_type == "date":
            right_operand = rule["value_date"]
        elif field.field_type == "time":
            right_operand = rule["value_time"]
        elif field.field_type == "datetime":
            right_operand = rule["value_datetime"]
        else:  # checkbox, file, label
            right_operand = ""

        func = OPERATIONS[rule["operator"]]

        try:
            return func(left_operand, right_operand)
        except Exception:
            print("error when solving rule:", left_operand, rule["operator"], right_operand)
            return False

    def get_active_fields(self, form_data: dict[str, Any]) -> list[str]:
        """Return the list of fields slug where the computed conditional value of the field is true."""

        def get_choices(field: BaseField) -> StrDict:
            if "choices" not in field.options:
                return {}

            fmt_options = StreamFieldFormBuilder.format_field_options(field.options)
            return {f"c{idx + 1}": choice[0] for idx, choice in enumerate(fmt_options["choices"])}

        fields_dict = self.get_form_fields_dict()
        choices_slugs = {field_id: get_choices(field) for field_id, field in fields_dict.items()}
        slugs = {field_id: field.clean_name for field_id, field in fields_dict.items()}

        active_fields = []
        for field in fields_dict.values():
            rules = field.options["rule"]
            if not rules or (
                self.process_rule(form_data, choices_slugs, rules[0])
                and (
                    rules[0]["field"] in ["and", "or"] or slugs[rules[0]["field"]] in active_fields
                )
            ):
                active_fields.append(field.clean_name)

        return active_fields

    class Meta:  # type: ignore
        abstract = True
