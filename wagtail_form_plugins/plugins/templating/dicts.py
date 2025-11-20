"""A set a typed dict used for better type hints in the Templating plugin."""

from typing import TypedDict


class UserDataDict(TypedDict):
    """A typed dict containing user data, used for instance in the {{user.xxx}} template syntax."""

    login: str
    first_name: str
    last_name: str
    full_name: str
    email: str


class FormDataDict(TypedDict):
    """A typed dict containing user data, used in {{form.xxx}} template syntax."""

    title: str
    url: str
    publish_date: str
    publish_time: str
    url_results: str


class ResultDataDict(TypedDict):
    """A typed dict containing user data, used in {{result.xxx}} template syntax."""

    data: str
    publish_date: str
    publish_time: str


class DataDict(TypedDict):
    """A typed dict containing format data, used in template syntax key prefixes."""

    user: UserDataDict
    author: UserDataDict
    form: FormDataDict
    result: ResultDataDict | None
    field_label: dict[str, str]
    field_value: dict[str, str]
