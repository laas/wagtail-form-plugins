from wagtail_form_plugins.base.models import FormMixin

from .formatter import TemplatingFormatter


class TemplatingFormMixin(FormMixin):
    formatter_class = TemplatingFormatter

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        formatter = self.formatter_class(response.context_data)

        if request.method == "GET":
            for field in response.context_data["form"].fields.values():
                if field.initial:
                    field.initial = formatter.format(field.initial)

        if "form_submission" in response.context_data:
            for email in response.context_data["page"].emails_to_send:
                for field_name in ["subject", "message", "recipient_list", "reply_to"]:
                    email.value[field_name] = formatter.format(str(email.value[field_name]))

        return response

    class Meta:
        abstract = True
