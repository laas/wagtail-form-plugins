"""A set a typed dict used for better type hints in the Conditional Fields plugin."""

from datetime import date, datetime, time
from typing import Literal, TypedDict

from typing_extensions import LiteralString, NotRequired


class EntryDict(TypedDict):
    """A typed dict corresponding to the entry attribute in the FormattedRuleDict."""

    target: str
    val: int | str
    opr: str


class FormattedRuleDict(TypedDict):
    """A typed dict corresponding to the object that will inserted to conditional fields as json."""

    entry: NotRequired[EntryDict]
    bool_opr: NotRequired[Literal["and", "or"]]
    subrules: NotRequired[list["FormattedRuleDict"]]


class RuleBlockDict(TypedDict):
    """A typed dict containing the value entry, used internaly in wagtail blocks."""

    value: "RuleBlockValueDict"


class RuleBlockValueDict(TypedDict):
    """A typed dict containing field displayed values in a Rule block."""

    field: LiteralString
    operator: str
    value_char: str
    value_number: int
    value_dropdown: str
    value_date: date
    value_time: time
    value_datetime: datetime
    rules: list[RuleBlockDict]
