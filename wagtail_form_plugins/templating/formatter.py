from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.utils import get_field_clean_name

TMPL_SEP_LEFT = "{"
TMPL_SEP_RIGHT = "}"
TMPL_DYNAMIC_PREFIXES = ["field_label", "field_value"]


class TemplatingFormatter:
    def __init__(self, context):
        self.submission = context.get("form_submission", None)
        self.form = context["page"]
        self.request = context["request"]
        self.data = self.get_data()
        self.values = self.get_values()

    def get_data(self):
        data = {
            "user": self.get_user_data(self.request.user),
            "author": self.get_user_data(self.form.owner),
            "form": self.get_form_data(),
        }

        if self.submission:
            formated_fields = self.get_formated_fields()

            data["result"] = self.get_result_data(formated_fields)
            data["field_label"] = {id: label for id, [label, value] in formated_fields.items()}
            data["field_value"] = {id: value for id, [label, value] in formated_fields.items()}

        return data

    def get_values(self):
        values = {}

        for val_name, value in self.data.items():
            if isinstance(value, dict):
                for sub_val_name, sub_value in value.items():
                    values[f"{val_name}.{sub_val_name}"] = str(sub_value)
            else:
                values[val_name] = str(value)

        return values

    def get_formated_fields(self):
        fields = {}
        for field in self.form.form_fields:
            if field.block.name == "hidden":
                continue
            field_label = field.value["label"]
            field_slug = get_field_clean_name(field_label)
            value = self.submission.form_data[field_slug]
            if value is None:
                continue
            fmt_value = self.form.format_field_value(field.block.name, value)
            fields[field_slug] = (field_label, fmt_value)
        return fields

    def get_user_data(self, user):
        is_anonymous = isinstance(user, AnonymousUser)
        return {
            "login": user.username,
            "first_name": "" if is_anonymous else user.first_name,
            "last_name": "" if is_anonymous else user.last_name,
            "full_name": "" if is_anonymous else f"{ user.first_name } {user.last_name }",
            "email": "" if is_anonymous else user.email,
        }

    def get_form_data(self):
        return {
            "title": self.form.title,
            "url": self.request.build_absolute_uri(self.form.url),
            "publish_date": self.form.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": self.form.first_published_at.strftime("%H:%M"),
        }

    def get_result_data(self, formated_fields):
        return {
            "data": "<br/>\n".join(
                [f"{label}: {value}" for label, value in formated_fields.values()]
            ),
            "publish_date": self.submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": self.submission.submit_time.strftime("%H:%M"),
        }

    def format(self, message):
        for val_key, value in self.values.items():
            look_for = TMPL_SEP_LEFT + val_key + TMPL_SEP_RIGHT
            if look_for in message:
                message = message.replace(look_for, value)
        return message

    @classmethod
    def doc(cls):
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
    def help(cls):
        doc = cls.doc()
        help_message = ""

        for tmpl_prefix, item in doc.items():
            help_message += "\n"
            for tmpl_suffix, (help_text, example) in item.items():
                key = f"{ TMPL_SEP_LEFT }{ tmpl_prefix }.{ tmpl_suffix }{ TMPL_SEP_RIGHT }"
                value = f"{ help_text } (ex: “{ example }”)"
                help_message += f"• { key }: { value }\n"

        return help_message

    @classmethod
    def contains_template(cls, text: str) -> bool:
        for tmpl_prefix, tmpl_suffixes in cls.doc().items():
            if tmpl_prefix in TMPL_DYNAMIC_PREFIXES:
                continue

            for tmpl_suffix in tmpl_suffixes:
                template = f"{ TMPL_SEP_LEFT }{ tmpl_prefix }.{ tmpl_suffix }{ TMPL_SEP_RIGHT }"
                if template in text:
                    return True

        for tmpl_prefix in TMPL_DYNAMIC_PREFIXES:
            sep = f"{ TMPL_SEP_LEFT }{ tmpl_prefix }."
            tmpl_suffix = (text.split(sep, 1) + [""])[1].split(TMPL_SEP_RIGHT, 1)[0]
            if tmpl_suffix:
                if tmpl_suffix != get_field_clean_name(tmpl_suffix):
                    raise ValueError
                return True

        if TMPL_SEP_LEFT in text or TMPL_SEP_RIGHT in text:
            raise ValueError

        return False
