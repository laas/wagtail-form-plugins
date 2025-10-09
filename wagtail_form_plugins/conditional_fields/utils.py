from datetime import date, datetime, time, timezone
from typing import Literal, TypedDict

from typing_extensions import NotRequired


def get_date_timestamp(value: date | str | None) -> int:
    if not value:
        value_dt = datetime.now()
    elif isinstance(value, str):
        value_dt = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        value_dt = datetime.combine(value, datetime.min.time())
    return int(value_dt.timestamp())


def get_time_timestamp(value: time | str | None) -> int:
    if not value:
        value_dt = datetime.now()
    elif isinstance(value, str):
        value_dt = datetime.fromisoformat(f"1970-01-01T{value}")
    else:
        value_dt = datetime.combine(date(1970, 1, 1), value)
    return int(value_dt.timestamp())


def get_datetime_timestamp(value: datetime | str | None) -> int:
    if not value:
        value_dt = datetime.now()
    elif isinstance(value, str):
        value_dt = datetime.fromisoformat(value)
    else:
        value_dt = value
    return int(value_dt.timestamp())


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
