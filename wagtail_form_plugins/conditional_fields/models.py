"""Models definition for the Conditional Fields form plugin."""

import json
from collections.abc import Callable
from typing import Any

from django.forms import BaseForm

from wagtail_form_plugins.streamfield import StreamFieldFormPage
from wagtail_form_plugins.utils import AnyDict

from . import ConditionalFieldsFormField, utils

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


class ConditionalFieldsFormPage(StreamFieldFormPage):
    """Form page used to add conditional fields functionnality to a form."""

    def get_form(self, *args, **kwargs) -> BaseForm:
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)
        form_fields: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # type: ignore

        for field_value in form.fields.values():
            form_field = form_fields[field_value.slug]  # type: ignore
            rule = form_field.rule
            if rule:
                field_value.widget.attrs.update(
                    {
                        "id": form_field.block_id,
                        "data-label": form_field.label,
                        "data-type": form_field.type,
                        "data-rule": json.dumps(rule),
                    }
                )

        form.full_clean()
        return form

    def get_right_operand(
        self, field: ConditionalFieldsFormField, leaf_rule: utils.RuleBlockValueDict
    ) -> str | int:
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
            return utils.get_date_timestamp(leaf_rule["value_date"])
        if field.type == "time":
            return utils.get_time_timestamp(leaf_rule["value_time"])
        if field.type == "datetime":
            return utils.get_datetime_timestamp(leaf_rule["value_datetime"])
        return ""

    # TODO: typer form_data
    def process_rule(
        self,
        fields: dict[str, ConditionalFieldsFormField],
        form_data: AnyDict,
        rule: utils.RuleBlockValueDict,
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
        fields_dict: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # type: ignore

        new_enabled_fields = []
        for field_slug in enabled_fields:
            field = fields_dict[field_slug]
            rules: list[utils.RuleBlockValueDict] = field.options.get("rule", [])

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
