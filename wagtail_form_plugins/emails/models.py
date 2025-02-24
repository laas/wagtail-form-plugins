"""Models definition for the Emails form plugin."""

from typing import Any
from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings
from django.utils.html import strip_tags


from wagtail_form_plugins.base.models import FormMixin


class EmailActionsFormMixin(FormMixin):
    """Form mixin for the EmailActions plugin, allowing to send emails when submitting a form."""

    def serve(self, request: HttpRequest, *args, **kwargs):
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect):
            return response

        if "form_submission" in response.context_data:
            for email in response.context_data["page"].emails_to_send:
                self.send_action_email(email.value)

        return response

    def send_action_email(self, email: dict[str, Any]):
        """Send an email"""
        email = {
            "subject": email["subject"],
            "recipient_list": [ea.strip() for ea in email["recipient_list"].split(",")],
            "reply_to": [ea.strip() for ea in email["reply_to"].split(",")],
            "from_email": settings.FORMS_FROM_EMAIL,
            "message": strip_tags(email["message"].replace("</p>", "</p>\n")),
            "html_message": email["message"],
        }
        super().send_email(email)

    class Meta:
        abstract = True
