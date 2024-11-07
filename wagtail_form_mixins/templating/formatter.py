from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.utils import get_field_clean_name

TEMPLATE_VAR_LEFT = "{"
TEMPLATE_VAR_RIGHT = "}"


class TemplatingFormatter:
    def __init__(self, context):
        self.submission = context.get("form_submission", None)
        self.form = context["page"]
        self.request = context["request"]
        self.fields_data = self.get_fields_data() if self.submission else None
        self.data = self.load_data()
        self.values = self.load_values()

    def load_data(self):
        data = {
            "user": self.load_user_data(self.request.user),
            "author": self.load_user_data(self.form.owner),
            "form": self.load_form_data(),
        }

        if self.submission:
            data["result"] = self.load_result_data()
            data["field_label"] = self.load_label_data()
            data["field_value"] = self.load_value_data()

        return data

    def load_values(self):
        values = {}

        for val_name, value in self.data.items():
            if isinstance(value, dict):
                for sub_val_name, sub_value in value.items():
                    values[f"{val_name}.{sub_val_name}"] = str(sub_value)
            else:
                values[val_name] = str(value)

        return values

    def get_fields_data(self):
        fields = {}
        for field in self.form.form_fields:
            field_label = field.value["label"]
            field_slug = get_field_clean_name(field_label)
            value = self.submission.form_data[field_slug]
            fmt_value = self.form.format_field_value(field.block.name, value)
            fields[field_slug] = (field_label, fmt_value)
        return fields

    def load_user_data(self, user):
        is_anonymous = isinstance(user, AnonymousUser)
        return {
            "login": user.username,
            "first_name": "" if is_anonymous else user.first_name,
            "last_name": "" if is_anonymous else user.last_name,
            "full_name": "" if is_anonymous else f"{ user.first_name } {user.last_name }",
            "email": "" if is_anonymous else user.email,
        }

    def load_form_data(self):
        return {
            "title": self.form.title,
            "url": self.request.build_absolute_uri(self.form.url),
            "publish_date": self.form.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": self.form.first_published_at.strftime("%H:%M"),
        }

    def load_label_data(self):
        return {id: label for id, [label, value] in self.fields_data.items()}

    def load_value_data(self):
        return {id: value for id, [label, value] in self.fields_data.items()}

    def load_result_data(self):
        return {
            "data": "<br/>\n".join(
                [f"{label}: {value}" for label, value in self.fields_data.values()]
            ),
            "publish_date": self.submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": self.submission.submit_time.strftime("%H:%M"),
        }

    def format(self, message):
        for val_key, value in self.values.items():
            look_for = TEMPLATE_VAR_LEFT + val_key + TEMPLATE_VAR_RIGHT
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

        for var_prefix, item in doc.items():
            help_message += "\n"
            for var_suffix, (help_text, example) in item.items():
                key = f"{{{ var_prefix }.{ var_suffix }}}"
                value = f"{ help_text } (ex: “{ example }”)"
                help_message += f"• { key }: { value }\n"

        return help_message

    @classmethod
    def examples(cls):
        doc = cls.doc()
        examples = {}

        for var_prefix, item in doc.items():
            for var_suffix, (help_text, example) in item.items():
                examples[f"{{{ var_prefix }.{ var_suffix }}}"] = example

        return examples
