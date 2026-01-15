"""Define the ConditionalFieldsFormField data class, representing a field with a rule attribute."""

from dataclasses import dataclass

from wagtail_form_plugins.streamfield.dicts import StreamFieldDataDict, StreamFieldValueDict
from wagtail_form_plugins.streamfield.form_field import StreamFieldFormField

from .dicts import FormattedRuleDict, RuleBlockDict, RuleBlockValueDict
from .utils import date_to_timestamp, datetime_to_timestamp, time_to_timestamp

from typing_extensions import Self


class ConditionalFieldsValueDict(StreamFieldValueDict):
    """A typed dict that holds a stream field data."""

    rule: list[RuleBlockDict]


@dataclass
class ConditionalFieldsFormField(StreamFieldFormField):
    """Add the rule attribute to the form field object."""

    rule: FormattedRuleDict | None = None

    @classmethod
    def from_streamfield_data(cls, field_data: StreamFieldDataDict) -> Self:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        data = super().from_streamfield_data(field_data)

        field_value: ConditionalFieldsValueDict = field_data["value"]  # ty: ignore[invalid-assignment]
        field_rule = field_value["rule"]
        data.rule = cls.format_rule(field_rule[0]["value"]) if field_rule else None

        return data

    @classmethod
    def format_rule(cls, rule: RuleBlockValueDict) -> FormattedRuleDict:
        """Recusively format a field rule in order to facilitate its parsing on the client side."""
        if rule["field"] in ("and", "or"):
            rules = [cls.format_rule(_rule["value"]) for _rule in rule["rules"]]
            return {"bool_opr": rule["field"], "subrules": rules}

        if rule["value_char"]:
            fmt_value = rule["value_char"]
        if rule["value_date"]:
            fmt_value = date_to_timestamp(rule["value_date"])
        elif rule["value_time"]:
            fmt_value = time_to_timestamp(rule["value_time"])
        elif rule["value_datetime"]:
            fmt_value = datetime_to_timestamp(rule["value_datetime"])
        elif rule["value_number"]:
            fmt_value = int(rule["value_number"])
        else:
            fmt_value = rule["value_dropdown"]

        return {
            "entry": {
                "target": rule["field"],
                "val": fmt_value,
                "opr": rule["operator"],
            },
        }
