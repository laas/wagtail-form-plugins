"""Classes and variables used to format the template syntax."""

from typing import Any, TypedDict

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.utils.translation import gettext as _

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.contrib.forms.models import FormSubmission

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage
from wagtail_form_plugins.utils import StrDict, create_links, validate_identifier

TMPL_SEP_LEFT = "{"
TMPL_SEP_RIGHT = "}"
TMPL_DYNAMIC_PREFIXES = ["field_label", "field_value"]


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
    field_label: StrDict
    field_value: StrDict


class TemplatingFormatter:
    """Class used to format the template syntax."""

    def __init__(self, context: dict[str, Any]):
        self.submission: FormSubmission | None = context.get("form_submission", None)
        self.form_page: StreamFieldFormPage = context["page"]
        self.request: HttpRequest = context["request"]

    def get_data(self, in_html: bool) -> DataDict:
        """Return the template data. Override to customize template."""
        formated_fields = self.get_formated_fields(in_html)
        return {
            "user": self.get_user_data(self.request.user),  # type: ignore
            "author": self.get_user_data(self.form_page.owner),
            "form": self.get_form_data(),
            "result": self.get_result_data(formated_fields),
            "field_label": {f_id: f_label for f_id, [f_label, f_value] in formated_fields.items()},
            "field_value": {f_id: f_value for f_id, [f_label, f_value] in formated_fields.items()},
        }

    def get_values(self, in_html: bool) -> StrDict:
        """Return a dict containing all formatter values on the root level."""
        values = {}

        for val_name, value in self.get_data(in_html).items():
            if isinstance(value, dict):
                for sub_val_name, sub_value in value.items():
                    values[f"{val_name}.{sub_val_name}"] = sub_value
            else:
                values[val_name] = value

        return values

    def get_formated_fields(self, in_html: bool = False) -> dict[str, tuple[str, str]]:
        """Return a dict containing a tuple of label and formatted value for each form field."""
        if not self.submission:
            return {}

        fields = {}
        enabled_fields = self.form_page.get_enabled_fields(self.submission.form_data)

        for field in self.form_page.get_form_fields():
            if field.slug not in enabled_fields:
                continue

            value = self.submission.form_data[field.slug]
            fmt_value = self.form_page.format_field_value(field, value, True, in_html)
            if fmt_value is not None:
                fields[field.slug] = (field.label, fmt_value)

        return fields

    def get_user_data(self, user: User) -> UserDataDict:
        """Return a dict used to format template variables related to the form user or author."""
        is_anonymous = isinstance(user, AnonymousUser)
        return {
            "login": user.username,
            "first_name": "" if is_anonymous else user.first_name,
            "last_name": "" if is_anonymous else user.last_name,
            "full_name": "" if is_anonymous else f"{user.first_name} {user.last_name}",
            "email": "" if is_anonymous else user.email,
        }

    def get_form_data(self) -> FormDataDict:
        """Return a dict used to format template variables related to the form itself."""
        finder = AdminURLFinder()
        return {
            "title": self.form_page.title,
            "url": self.request.build_absolute_uri(self.form_page.url),
            "publish_date": self.form_page.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": self.form_page.first_published_at.strftime("%H:%M"),
            "url_results": settings.WAGTAILADMIN_BASE_URL + finder.get_edit_url(self.form_page),
        }

    # class Result
    def get_result_data(self, formated_fields: dict[str, tuple[str, str]]) -> ResultDataDict | None:
        """Return a dict used to format template variables related to the form results."""
        if not self.submission:
            return None

        return {
            "data": "<br/>\n".join([f"◦ {lbl}: {val}" for lbl, val in formated_fields.values()]),
            "publish_date": self.submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": self.submission.submit_time.strftime("%H:%M"),
        }

    def format(self, message: str, in_html: bool) -> str:
        """Format the message template by replacing template variables."""
        for val_key, value in self.get_values(in_html).items():
            look_for = TMPL_SEP_LEFT + val_key + TMPL_SEP_RIGHT
            if look_for in message:
                message = message.replace(look_for, value)

        if in_html:
            message = create_links(message.replace("\n", "<br/>\n"))

        return message

    @classmethod
    def doc(cls) -> dict[str, dict[str, tuple[str, str]]]:
        """Return the dict used to build the template documentation."""
        return {
            "user": {
                "login": (_("the form user login"), "alovelace"),
                "email": (_("the form user email"), "alovelace@example.com"),
                "first_name": (_("the form user first name"), "Ada"),
                "last_name": (_("the form user last name"), "Lovelace"),
                "full_name": (_("the form user first name and last name"), "Ada Lovelace"),
            },
            "author": {
                "login": (_("the form author login"), "shawking"),
                "email": (_("the form author email"), "alovelace@example.com"),
                "first_name": (_("the form author first name"), "Stephen"),
                "last_name": (_("the form author last name"), "Hawking"),
                "full_name": (_("the form author first name and last name"), "Stephen Hawking"),
            },
            "form": {
                "title": (_("the form title"), "My form"),
                "url": (_("the form url"), "https://example.com/form/my-form"),
                "publish_date": (_("the date on which the form was published"), "15/10/2024"),
                "publish_time": (_("the time on which the form was published"), "13h37"),
                "url_results": (
                    _("the url of the form edition page"),
                    "https://example.com/admin/pages/42/edit/",
                ),
            },
            "result": {
                "data": (_("the form data as a list"), "- my_first_question: 42"),
                "publish_date": (_("the date on which the form was completed"), "16/10/2024"),
                "publish_time": (_("the time on which the form was completed"), "12h06"),
            },
            "field_label": {
                "my_first_question": (_("the label of the related field"), "My first question"),
            },
            "field_value": {
                "my_first_question": (_("the value of the related field"), "42"),
            },
        }

    @classmethod
    def help(cls) -> str:
        """Build the template help message."""
        doc = cls.doc()
        help_message = ""

        for tmpl_prefix, item in doc.items():
            help_message += "\n"
            for tmpl_suffix, (help_text, example) in item.items():
                key = f"{TMPL_SEP_LEFT}{tmpl_prefix}.{tmpl_suffix}{TMPL_SEP_RIGHT}"
                value = f"{help_text} (ex: “{example}”)"
                help_message += f"• {key}: {value}\n"

        return help_message

    @classmethod
    def contains_template(cls, text: str) -> bool:
        """Return True if the given text contain a template, False otherwise."""
        for tmpl_prefix, tmpl_suffixes in cls.doc().items():
            if tmpl_prefix in TMPL_DYNAMIC_PREFIXES:
                continue

            for tmpl_suffix in tmpl_suffixes:
                template = f"{TMPL_SEP_LEFT}{tmpl_prefix}.{tmpl_suffix}{TMPL_SEP_RIGHT}"
                if template in text:
                    return True

        for tmpl_prefix in TMPL_DYNAMIC_PREFIXES:
            sep = f"{TMPL_SEP_LEFT}{tmpl_prefix}."
            tmpl_suffix = [*text.split(sep, 1), ""][1].split(TMPL_SEP_RIGHT, 1)[0]
            if tmpl_suffix:
                validate_identifier(tmpl_suffix)
                return True

        if TMPL_SEP_LEFT in text or TMPL_SEP_RIGHT in text:
            raise ValueError

        return False
