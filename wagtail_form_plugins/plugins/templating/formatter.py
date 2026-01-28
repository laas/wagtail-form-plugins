"""Classes and variables used to format the template syntax."""

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.utils.html import format_html
from django.utils.translation import gettext as _

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.panels import RichText

from wagtail_form_plugins.streamfield.models import StreamFieldFormatter
from wagtail_form_plugins.utils import format_list, validate_slug

from .dicts import DataDict, FormDataDict, ResultDataDict, UserDataDict

TMPL_SEP_LEFT = "{"
TMPL_SEP_RIGHT = "}"
TMPL_DYNAMIC_PREFIXES = ["field_label", "field_value"]


class TemplatingFormatter(StreamFieldFormatter):
    """Class used to format the template syntax."""

    def get_data(self) -> DataDict:
        """Return the template data. Override to customize template."""
        formated_fields = self.get_formated_fields()
        return {
            "user": self.get_user_data(self.user),
            "author": self.get_user_data(self.form_page.owner),
            "form": self.get_form_data(),
            "result": self.get_result_data(formated_fields),
            "field_label": {f_id: f_label for f_id, [f_label, f_value] in formated_fields.items()},
            "field_value": {f_id: f_value for f_id, [f_label, f_value] in formated_fields.items()},
        }

    def get_values(self) -> dict[str, str]:
        """Return a dict containing all formatter values on the root level."""
        values = {}

        for key_prefix, value in self.get_data().items():
            if isinstance(value, dict):
                for key_suffix, sub_value in value.items():
                    values[f"{key_prefix}.{key_suffix}"] = sub_value

        return values

    def get_formated_fields(self) -> dict[str, tuple[str, str]]:
        """Return a dict containing a tuple of label and formatted value for each form field."""
        if not self.submission:
            return {}

        fmt_fields = {}
        enabled_fields = self.form_page.get_enabled_fields(self.submission.form_data)

        for field in self.form_page.get_form_fields():
            if field.slug not in enabled_fields:
                continue

            value = self.submission.form_data[field.slug]
            fmt_value = self.form_page.format_field_value(field, value, in_html=self.in_html)
            if fmt_value is not None:
                fmt_fields[field.slug] = (field.label, fmt_value)

        return fmt_fields

    def get_user_data(self, user: User) -> UserDataDict:
        """Return a dict used to format template variables related to the form user or author."""
        is_logged = not isinstance(user, AnonymousUser) and user is not None

        return {
            "login": user.username if is_logged else "",
            "first_name": user.first_name if is_logged else "",
            "last_name": user.last_name if is_logged else "",
            "full_name": f"{user.first_name} {user.last_name}" if is_logged else "",
            "email": user.email if is_logged else "",
        }

    def get_form_data(self) -> FormDataDict:
        """Return a dict used to format template variables related to the form itself."""
        finder = AdminURLFinder()

        return {
            "title": self.form_page.title,
            "url": settings.WAGTAILADMIN_BASE_URL + self.form_page.url,
            "publish_date": self.form_page.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": self.form_page.first_published_at.strftime("%H:%M"),
            "url_results": settings.WAGTAILADMIN_BASE_URL + finder.get_edit_url(self.form_page),
        }

    def get_result_data(self, formated_fields: dict[str, tuple[str, str]]) -> ResultDataDict | None:
        """Return a dict used to format template variables related to the form results."""
        if not self.submission:
            return None

        values = [
            format_html("{lbl}: {val}", lbl=lbl, val=val) for lbl, val in formated_fields.values()
        ]
        fmt_list = format_list(values, "◦", in_html=self.in_html)

        return {
            "data": fmt_list,
            "publish_date": self.submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": self.submission.submit_time.strftime("%H:%M"),
        }

    def format(self, message: str | RichText) -> str:
        """Format the message template by replacing template variables."""
        fmt_message = str(message)
        for val_key, value in self.get_values().items():
            look_for = TMPL_SEP_LEFT + val_key + TMPL_SEP_RIGHT
            if look_for in fmt_message:
                replaced = "" if value is None else str(value)
                fmt_message = fmt_message.replace(look_for, replaced)

        # handle disabled fields
        for field in self.form_page.get_form_fields():
            look_for = TMPL_SEP_LEFT + "field_value." + field.slug + TMPL_SEP_RIGHT
            if look_for in fmt_message:
                fmt_message = fmt_message.replace(look_for, "---")

            look_for = TMPL_SEP_LEFT + "field_label." + field.slug + TMPL_SEP_RIGHT
            if look_for in fmt_message:
                fmt_message = fmt_message.replace(look_for, field.label)

        return fmt_message

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
                validate_slug(tmpl_suffix)
                return True

        if TMPL_SEP_LEFT in text or TMPL_SEP_RIGHT in text:
            raise ValueError

        return False
