from datetime import date, datetime, time
from typing import Literal, TypedDict

from typing_extensions import NotRequired


class EntryDict(TypedDict):
    target: str
    val: int | str
    opr: str


class FormattedRuleDict(TypedDict):
    entry: NotRequired[EntryDict]
    bool_opr: NotRequired[Literal["and", "or"]]
    subrules: NotRequired[list["FormattedRuleDict"]]


class RuleBlockDict(TypedDict):
    value: "RuleBlockValueDict"


class RuleBlockValueDict(TypedDict):
    field: str
    operator: str
    value_char: str
    value_number: int
    value_dropdown: str
    value_date: date
    value_time: time
    value_datetime: datetime
    rules: list[RuleBlockDict]
