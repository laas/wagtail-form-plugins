from dataclasses import dataclass

from wagtail_form_plugins.conditional_fields import utils
from wagtail_form_plugins.conditional_fields.models import FormattedRuleDict
from wagtail_form_plugins.streamfield import FormField, StreamFieldFormBuilder

from .blocks import RuleBlockValueDict


@dataclass
class ConditionalFieldsFormField(FormField):
    @property
    def get_rule(self) -> FormattedRuleDict | None:
        raw_rule = self.options.get("rule", None)
        return self.format_rule(raw_rule[0]["value"]) if raw_rule else None

    @classmethod
    def format_rule(cls, rule: RuleBlockValueDict) -> FormattedRuleDict:
        """Recusively format a field rule in order to facilitate its parsing on the client side."""

        if rule["field"] in ("and", "or"):
            rules = [cls.format_rule(_rule["value"]) for _rule in rule["rules"]]
            return {"bool_opr": rule["field"], "subrules": rules}

        if rule["value_date"]:
            fmt_value = utils.get_date_timestamp(rule["value_date"])
        elif rule["value_time"]:
            fmt_value = utils.get_time_timestamp(rule["value_time"])
        elif rule["value_datetime"]:
            fmt_value = utils.get_datetime_timestamp(rule["value_datetime"])
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


class ConditionalFieldsFormBuilder(StreamFieldFormBuilder):
    def __init__(self, fields: list[FormField]):
        super().__init__(fields)
        self.extra_field_options += ["rule"]
