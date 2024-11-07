from django.contrib.auth.models import AnonymousUser

from wagtail.contrib.forms.utils import get_field_clean_name

TEMPLATE_VAR_LEFT = "{"
TEMPLATE_VAR_RIGHT = "}"


class BaseFormatter:
    def __init__(self, data):
        self.values = {}

        for val_name, value in data.items():
            if isinstance(value, dict):
                for sub_val_name, sub_value in value.items():
                    self.values[f"{val_name}.{sub_val_name}"] = str(sub_value)
            else:
                self.values[val_name] = str(value)

    def format(self, message):
        for val_key, value in self.values.items():
            look_for = TEMPLATE_VAR_LEFT + val_key + TEMPLATE_VAR_RIGHT
            if look_for in message:
                message = message.replace(look_for, value)
        return message


class TemplatingFormatter(BaseFormatter):
    def __init__(self, context):
        self.submission = context.get("form_submission", None)
        self.form = context["page"]
        self.request = context["request"]
        self.fields_data = self.get_fields_data() if self.submission else None

        data = {
            "user": self.format_user(self.request.user),
            "author": self.format_user(self.form.owner),
            "form": self.format_form(),
        }

        if self.submission:
            data["result"] = self.format_result()
            data["field_label"] = self.format_label()
            data["field_value"] = self.format_value()

        super().__init__(data)

    def get_fields_data(self):
        fields = {}
        for field in self.form.form_fields:
            field_label = field.value["label"]
            field_slug = get_field_clean_name(field_label)
            value = self.submission.form_data[field_slug]
            fmt_value = self.form.format_field_value(field.block.name, value)
            fields[field_slug] = (field_label, fmt_value)
        return fields

    def format_user(self, user):
        is_anonymous = isinstance(user, AnonymousUser)
        return {
            "login": user.username,
            "first_name": "" if is_anonymous else user.first_name,
            "last_name": "" if is_anonymous else user.last_name,
            "full_name": "" if is_anonymous else f"{ user.first_name } {user.last_name }",
            "email": "" if is_anonymous else user.email,
        }

    def format_form(self):
        return {
            "title": self.form.title,
            "url": self.request.build_absolute_uri(self.form.url),
            "publish_date": self.form.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": self.form.first_published_at.strftime("%H:%M"),
        }

    def format_label(self):
        return {id: label for id, [label, value] in self.fields_data.items()}

    def format_value(self):
        return {id: value for id, [label, value] in self.fields_data.items()}

    def format_result(self):
        return {
            "data": "<br/>\n".join(
                [f"{label}: {value}" for label, value in self.fields_data.values()]
            ),
            "publish_date": self.submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": self.submission.submit_time.strftime("%H:%M"),
        }
