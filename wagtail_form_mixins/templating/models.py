from wagtail.contrib.forms.utils import get_field_clean_name


TEMPLATE_VAR_LEFT = "{"
TEMPLATE_VAR_RIGHT = "}"


class Context:
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


class FormContext(Context):
    def __init__(self, context):
        data = {
            "user": self.format_user(context["request"].user),
            "author": self.format_user(context["page"].owner),
            "form": self.format_form(context["page"], context["request"]),
        }

        if "form_submission" in context:
            fields = self.get_fields(context["form_submission"], context["page"].form_fields)
            data["result"] = self.format_result(context["form_submission"], fields)
            data["field_label"] = self.format_label(fields)
            data["field_value"] = self.format_value(fields)

        super().__init__(data)

    def get_fields(self, submission, form_fields):
        fields = {}
        for field in form_fields:
            field_label = field.value["label"]
            field_id = get_field_clean_name(field_label)
            field_value = submission.form_data[field_id]
            fields[field_id] = (field_label, field_value)
        return fields

    def format_user(self, user):
        return {
            "login": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,
        }

    def format_form(self, form, request):
        return {
            "title": form.title,
            "url": request.build_absolute_uri(form.url),
            "publish_date": form.first_published_at.strftime("%d/%m/%Y"),
            "publish_time": form.first_published_at.strftime("%H:%M"),
        }

    def format_label(self, fields):
        return {id: label for id, [label, value] in fields.items()}

    def format_value(self, fields):
        return {id: value for id, [label, value] in fields.items()}

    def format_result(self, submission, fields):
        return {
            "data": "\n".join([f"{label}: {value}" for label, value in fields.values()]),
            "publish_date": submission.submit_time.strftime("%d/%m/%Y"),
            "publish_time": submission.submit_time.strftime("%H:%M"),
        }


class TemplatingFormMixin:
    template_context_class = FormContext

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        form_context = self.template_context_class(response.context_data)

        if request.method == "GET":
            for field in response.context_data["form"].fields.values():
                field.initial = form_context.format(field.initial)

        if "form_submission" in response.context_data:
            for email in response.context_data["page"].emails_to_send:
                for field_name in ["subject", "message", "recipient_list"]:
                    email.value[field_name] = form_context.format(str(email.value[field_name]))

        return response
