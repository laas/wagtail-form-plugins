"""Models definition for the Conditional Fields form plugin."""

import json
from collections.abc import Callable
from typing import Any

from django.contrib.auth.models import User
from django.forms import BaseForm

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage

from .dicts import FormattedRuleDict
from .form_field import ConditionalFieldsFormField

Operation = Callable[[Any, Any], bool]


OPERATIONS: dict[str, Operation] = {
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
    "is": lambda a, b: a == b,
    "nis": lambda a, b: a != b,
    "lt": lambda a, b: isinstance(a, int) and isinstance(b, int) and a < b,
    "lte": lambda a, b: isinstance(a, int) and isinstance(b, int) and a <= b,
    "ut": lambda a, b: isinstance(a, int) and isinstance(b, int) and a > b,
    "ute": lambda a, b: isinstance(a, int) and isinstance(b, int) and a >= b,
    "bt": lambda a, b: isinstance(a, int) and isinstance(b, int) and a < b,
    "bte": lambda a, b: isinstance(a, int) and isinstance(b, int) and a <= b,
    "at": lambda a, b: isinstance(a, int) and isinstance(b, int) and a > b,
    "ate": lambda a, b: isinstance(a, int) and isinstance(b, int) and a >= b,
    "ct": lambda a, b: isinstance(a, list) and b in a,
    "nct": lambda a, b: isinstance(a, list) and b not in a,
    "c": lambda a, _b: bool(a),
    "nc": lambda a, _b: not a,
}


class ConditionalFieldsFormPage(StreamFieldFormPage):
    """Form page used to add conditional fields functionnality to a form."""

    def get_form(self, *args, page: StreamFieldFormPage, user: User, **kwargs) -> BaseForm:
        """Build and return the form instance."""
        form = super().get_form(*args, page=page, user=user, **kwargs)

        form_fields: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # ty: ignore[ invalid-assignment]

        for field_slug, field_value in form.fields.items():
            form_field = form_fields[field_slug]
            if form_field.rule:
                field_value.widget.attrs["data-rule"] = json.dumps(form_field.rule)

        form.full_clean()
        return form

    def process_rule(
        self,
        fields: dict[str, ConditionalFieldsFormField],
        form_data: dict[str, Any],
        rule: FormattedRuleDict,
    ) -> bool:
        """Process the rule by applying the operator with left and right operands."""
        if "bool_opr" in rule and "subrules" in rule:
            results = [self.process_rule(fields, form_data, sr) for sr in rule["subrules"]]
            return all(results) if rule["bool_opr"] == "and" else any(results)

        if "entry" not in rule:
            msg = "Either an entry or a bool_opr + subrules should be stored in the rule dict."
            raise ValueError(msg)

        entry = rule["entry"]
        target_id = entry["target"] if "entry" in rule else None
        target_field = next(field for field in fields.values() if field.block_id == target_id)
        this_value = form_data[target_field.slug]
        that_value = entry["val"]

        func = OPERATIONS[entry["opr"]]

        try:
            return func(this_value, that_value)
        except Exception as err:
            msg = f"error when solving rule: {this_value} {entry['opr']} {that_value}"
            raise ArithmeticError(msg) from err

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        """Return the fields slug list where the computed conditional value of the field is true."""
        enabled_fields = super().get_enabled_fields(form_data)
        fields_dict: dict[str, ConditionalFieldsFormField] = self.get_form_fields_dict()  # ty: ignore[invalid-assignment]

        new_enabled_fields = []
        for field_slug in enabled_fields:
            field = fields_dict[field_slug]

            if field.rule is None:
                new_enabled_fields.append(field_slug)
                continue

            is_rule_true = self.process_rule(fields_dict, form_data, field.rule)
            target = field.rule["entry"]["target"] if "entry" in field.rule else None
            matches = [fld for fld in fields_dict.values() if fld.block_id == target]
            is_rule_field_enabled = "bool_opr" in field.rule or matches[0].slug in enabled_fields

            if is_rule_true and is_rule_field_enabled:
                new_enabled_fields.append(field_slug)

        return new_enabled_fields

    class Meta:
        abstract = True
