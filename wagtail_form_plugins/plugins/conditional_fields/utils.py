"""A set of utility functions used in the Conditional Fields plugin, mainly to format datetime."""

from datetime import date, datetime, time, timezone


def date_to_timestamp(value: date | str | None) -> int:
    """Return a timestamp based on a date object or stringified date."""
    if not value:
        value_dt = datetime.now(tz=timezone.utc)
    elif isinstance(value, str):
        value_dt = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        value_dt = datetime.combine(value, datetime.min.time())
    return int(value_dt.timestamp())


def time_to_timestamp(value: time | str | None) -> int:
    """Return a timestamp based on a time object or stringified time."""
    if not value:
        value_dt = datetime.now(tz=timezone.utc)
    elif isinstance(value, str):
        value_dt = datetime.fromisoformat(f"1970-01-01T{value}")
    else:
        value_dt = datetime.combine(date(1970, 1, 1), value)
    return int(value_dt.timestamp())


def datetime_to_timestamp(value: datetime | str | None) -> int:
    """Return a timestamp based on a datetime object or stringified datetime."""
    if not value:
        value_dt = datetime.now(tz=timezone.utc)
    elif isinstance(value, str):
        value_dt = datetime.fromisoformat(value)
    else:
        value_dt = value
    return int(value_dt.timestamp())
