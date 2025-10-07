from datetime import date, datetime, time, timezone


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
