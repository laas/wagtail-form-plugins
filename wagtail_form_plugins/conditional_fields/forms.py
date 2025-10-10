from dataclasses import dataclass

from wagtail_form_plugins.streamfield import StreamFieldFormBuilder, StreamFieldFormField

from .dicts import FormattedRuleDict, RuleBlockValueDict
from .utils import date_to_timestamp, datetime_to_timestamp, time_to_timestamp


@dataclass
class ConditionalFieldsFormField(StreamFieldFormField):
    _rule: FormattedRuleDict | None = None

    @property
    def rule(self) -> FormattedRuleDict | None:
        if self._rule is None:
            raw_rule = self.options.get("rule", None)
            self._rule = self.format_rule(raw_rule[0]["value"]) if raw_rule else None
        return self._rule

    def format_rule(self, rule: RuleBlockValueDict) -> FormattedRuleDict:
        """Recusively format a field rule in order to facilitate its parsing on the client side."""

        if rule["field"] in ("and", "or"):
            rules = [self.format_rule(_rule["value"]) for _rule in rule["rules"]]
            return {"bool_opr": rule["field"], "subrules": rules}

        if rule["value_date"]:
            fmt_value = date_to_timestamp(rule["value_date"])
        elif rule["value_time"]:
            fmt_value = time_to_timestamp(rule["value_time"])
        elif rule["value_datetime"]:
            fmt_value = datetime_to_timestamp(rule["value_datetime"])
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
    def __init__(self, fields: list[StreamFieldFormField]):
        super().__init__(fields)
        self.extra_field_options += ["rule"]
