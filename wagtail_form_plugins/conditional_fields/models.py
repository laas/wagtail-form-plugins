"""Models definition for the Conditional Fields form plugin."""

import json
from collections.abc import Callable
from datetime import date, datetime, time, timezone
from typing import Any, TypedDict

from django.forms import BaseForm

from wagtail_form_plugins.streamfield import StreamFieldFormPage
from wagtail_form_plugins.streamfield.forms import FormField
from wagtail_form_plugins.utils import AnyDict

from .blocks import RuleBlockValueDict

Operation = Callable[[Any, Any], bool]


OPERATIONS: dict[str, Operation] = {
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
    "c": lambda a, b: bool(a),
    "nc": lambda a, b: not a,
}


class EntryDict(TypedDict):
    target: str
    val: int | str
    opr: str


class FormattedRuleDict(TypedDict):
    entry: EntryDict


class ConditionalFieldsFormPage(StreamFieldFormPage):
    """Form page used to add conditional fields functionnality to a form."""

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        active_fields = []
        if args:
            form.full_clean()
            active_fields = self.get_enabled_fields(form.cleaned_data)

        form_fields = self.get_form_fields_dict()
        for field in form.fields.values():
            # print("form_field:", form_field.__dict__)
            # TODO: check from where slug come from
            form_field = form_fields[field.slug]  # type: ignore

            if "rule" not in form_field.options:
                continue

            if args and field.slug not in active_fields:  # type: ignore
                field.required = False

            # TODO: possible d'avoir field.rule plutôt, avec rule typé ?
            raw_rule = form_field.options["rule"]
            field_rule = self.format_rule(raw_rule[0]["value"]) if raw_rule else {}

            # TODO: changer "data-widget": ... par "data-type": field.type ?
            new_attributes = {
                "id": form_field.block_id,
                "data-label": field.label,
                "data-widget": field.widget.__class__.__name__,
                "data-rule": json.dumps(field_rule),
            }

            field.widget.attrs.update(new_attributes)

        form.full_clean()
        return form

    @classmethod
    def get_date_timestamp(cls, value: date | str | None) -> int:
        if not value:
            value_dt = datetime.now()
        elif isinstance(value, str):
            value_dt = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        else:
            value_dt = datetime.combine(value, datetime.min.time())
        return int(value_dt.timestamp())

    @classmethod
    def get_time_timestamp(cls, value: time | str | None) -> int:
        if not value:
            value_dt = datetime.now()
        elif isinstance(value, str):
            value_dt = datetime.fromisoformat(f"1970-01-01T{value}")
        else:
            value_dt = datetime.combine(date(1970, 1, 1), value)
        return int(value_dt.timestamp())

    @classmethod
    def get_datetime_timestamp(cls, value: datetime | str | None) -> int:
        if not value:
            value_dt = datetime.now()
        elif isinstance(value, str):
            value_dt = datetime.fromisoformat(value)
        else:
            value_dt = value
        return int(value_dt.timestamp())

    @classmethod
    def format_rule(cls, rule: RuleBlockValueDict) -> FormattedRuleDict:
        """Recusively format a field rule in order to facilitate its parsing on the client side."""

        if rule["field"] in ["and", "or"]:
            # TODO: change FormattedRuleDict format to avoid dynamic keys:
            # something like {entry: EntryDict, fields: list[FormattedRuleDict]}
            return {rule["field"]: [cls.format_rule(_rule["value"]) for _rule in rule["rules"]]}  # type: ignore

        if rule["value_date"]:
            fmt_value = cls.get_date_timestamp(rule["value_date"])
        elif rule["value_time"]:
            fmt_value = cls.get_time_timestamp(rule["value_time"])
        elif rule["value_datetime"]:
            fmt_value = cls.get_datetime_timestamp(rule["value_datetime"])
        elif rule["value_dropdown"]:
            fmt_value = rule["value_dropdown"]
        elif rule["value_number"]:
            fmt_value = int(rule["value_number"])
        else:
            fmt_value = rule["value_char"]

        return {
            "entry": {
                "target": rule["field"],
                "val": fmt_value,
                "opr": rule["operator"],
            },
        }

    def get_right_operand(self, field: FormField, leaf_rule: RuleBlockValueDict) -> str | int:
        """
        Return the right operand of the rule operation.
        The leaf_rule is a rule that does not contain a sub rule.
        """
        char_fields = ["singleline", "multiline", "email", "hidden", "url"]
        choice_fields = ["checkboxes", "dropdown", "multiselect", "radio"]

        if field.type in char_fields:
            return leaf_rule["value_char"]
        if field.type == "number":
            return int(leaf_rule["value_number"])
        if field.type in choice_fields:
            dropdown_val = leaf_rule["value_dropdown"]
            return field.choices[dropdown_val] if (dropdown_val and field.choices) else dropdown_val
        if field.type == "date":
            return self.get_date_timestamp(leaf_rule["value_date"])
        if field.type == "time":
            return self.get_time_timestamp(leaf_rule["value_time"])
        if field.type == "datetime":
            return self.get_datetime_timestamp(leaf_rule["value_datetime"])
        return ""

    # TODO: typer form_data
    def process_rule(
        self, fields: dict[str, FormField], form_data: AnyDict, rule: RuleBlockValueDict
    ) -> bool:
        rule_field_attr = rule["field"]

        if rule_field_attr in ["and", "or"]:
            results = [
                self.process_rule(fields, form_data, sub_rule["value"])
                for sub_rule in rule["rules"]
            ]
            return all(results) if rule_field_attr == "and" else any(results)

        field = next(field for field in fields.values() if field.block_id == rule_field_attr)

        func = OPERATIONS[rule["operator"]]
        left_operand = form_data[field.slug]
        # TODO: vérifier si form_data est bien formaté ici (date en timestamp, number en int, etc)
        right_operand = self.get_right_operand(field, rule)

        try:
            return func(left_operand, right_operand)
        except Exception:
            print("error when solving rule:", left_operand, rule["operator"], right_operand)
            return False

    def get_enabled_fields(self, form_data: AnyDict) -> list[str]:
        """Return the list of fields slug where the computed conditional value of the field is true."""
        enabled_fields = super().get_enabled_fields(form_data)
        fields_dict = self.get_form_fields_dict()

        new_enabled_fields = []
        for field_slug in enabled_fields:
            field = fields_dict[field_slug]
            rules: list[RuleBlockValueDict] = field.options.get("rule", [])

            if not rules:
                new_enabled_fields.append(field_slug)
                continue

            is_rule_true = self.process_rule(fields_dict, form_data, rules[0])
            field_attr = rules[0]["field"]
            rule_field = next(fld for fld in fields_dict.values() if fld.block_id == field_attr)
            is_rule_field_enabled = field_attr in ["and", "or"] or rule_field.slug in enabled_fields

            if is_rule_true and is_rule_field_enabled:
                new_enabled_fields.append(field_slug)

        return new_enabled_fields

    class Meta:  # type: ignore
        abstract = True
