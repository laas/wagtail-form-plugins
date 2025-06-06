"""Models definition for the Templating form plugin."""

from django.http import HttpRequest, HttpResponseRedirect
from wagtail_form_plugins.base.models import FormMixin

from .formatter import TemplatingFormatter


class TemplatingFormMixin(FormMixin):
    """Form mixin for the Templating plugin. Used to format initial values and submissions."""

    formatter_class = TemplatingFormatter

    def serve(self, request: HttpRequest, *args, **kwargs):
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect):
            return response

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
