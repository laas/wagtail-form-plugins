from typing import TypedDict


class UserDataDict(TypedDict):
    login: str
    first_name: str
    last_name: str
    full_name: str
    email: str


class FormDataDict(TypedDict):
    title: str
    url: str
    publish_date: str
    publish_time: str
    url_results: str


class ResultDataDict(TypedDict):
    data: str
    publish_date: str
    publish_time: str


class DataDict(TypedDict):
    user: UserDataDict
    author: UserDataDict
    form: FormDataDict
    result: ResultDataDict | None
    field_label: dict[str, str]
    field_value: dict[str, str]
