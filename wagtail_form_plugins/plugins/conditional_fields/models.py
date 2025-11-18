"""Models definition for the Conditional Fields form plugin."""

import json
from collections.abc import Callable
from typing import Any

from django.forms import BaseForm

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage
from wagtail_form_plugins.utils import LOGGER

from .dicts import RuleBlockDict, RuleBlockValueDict
from .form_field import ConditionalFieldsFormField
from .utils import date_to_timestamp, datetime_to_timestamp, time_to_timestamp

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
    "c": lambda a, _b: bool(a),
    "nc": lambda a, _b: not a,
}


class ConditionalFieldsFormPage(StreamFieldFormPage):
    """Form page used to add conditional fields functionnality to a form."""

    def get_form(self, *args, **kwargs) -> BaseForm:
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)
        form_fields: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # type: ignore[ invalid-assignment]

        for field_slug, field_value in form.fields.items():
            form_field = form_fields[field_slug]
            if form_field.rule:
                field_value.widget.attrs["data-rule"] = json.dumps(form_field.rule)

        form.full_clean()
        return form

    def get_right_operand(
        self,
        field: ConditionalFieldsFormField,
        leaf_rule: RuleBlockValueDict,
    ) -> str | int:
        """Return the right operand of the rule operation.
        The leaf_rule is a rule that does not contain a sub rule.
        """
        char_fields = ["singleline", "multiline", "email", "hidden", "url"]
        choice_fields = ["checkboxes", "dropdown", "multiselect", "radio"]

        right_operand = ""

        if field.type in char_fields:
            right_operand = leaf_rule["value_char"]
        elif field.type == "number":
            right_operand = int(leaf_rule["value_number"])
        elif field.type in choice_fields:
            dd_val = leaf_rule["value_dropdown"]
            choices = dict(field.choices)
            is_choice_valid = dd_val and choices and dd_val in choices
            right_operand = choices[dd_val] if is_choice_valid else dd_val
        elif field.type == "date":
            right_operand = date_to_timestamp(leaf_rule["value_date"])
        elif field.type == "time":
            right_operand = time_to_timestamp(leaf_rule["value_time"])
        elif field.type == "datetime":
            right_operand = datetime_to_timestamp(leaf_rule["value_datetime"])
        else:
            right_operand = ""

        return right_operand

    def process_rule(
        self,
        fields: dict[str, ConditionalFieldsFormField],
        form_data: dict[str, Any],
        rule: RuleBlockValueDict,
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
        right_operand = self.get_right_operand(field, rule)

        try:
            return func(left_operand, right_operand)
        except Exception:  # noqa: BLE001
            LOGGER.error("error when solving rule:", left_operand, rule["operator"], right_operand)
            return False

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        """Return the fields slug list where the computed conditional value of the field is true."""
        enabled_fields = super().get_enabled_fields(form_data)
        fields_dict: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # type: ignore[invalid-assignment]

        new_enabled_fields = []
        for field_slug in enabled_fields:
            field = fields_dict[field_slug]
            rules: list[RuleBlockDict] = field.options.get("rule", [])

            if not rules:
                new_enabled_fields.append(field_slug)
                continue

            is_rule_true = self.process_rule(fields_dict, form_data, rules[0]["value"])
            field_attr = rules[0]["value"]["field"]
            rule_field = next(fld for fld in fields_dict.values() if fld.block_id == field_attr)
            is_rule_field_enabled = field_attr in ["and", "or"] or rule_field.slug in enabled_fields

            if is_rule_true and is_rule_field_enabled:
                new_enabled_fields.append(field_slug)

        return new_enabled_fields

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        abstract = True
