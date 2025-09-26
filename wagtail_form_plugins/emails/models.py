"""Models definition for the Emails form plugin."""

from typing import Any

from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import strip_tags

from wagtail_form_plugins.base import BaseFormPage


class EmailActionsFormPage(BaseFormPage):
    """Form page for the EmailActions plugin, allowing to send emails when submitting a form."""

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        if "form_submission" in response.context_data:
            for email in response.context_data["page"].emails_to_send:
                self.send_action_email(email.value)

        return response

    def send_action_email(self, email: dict[str, Any]) -> None:
        """Send an e-mail"""
        self.send_mail(
            subject=email["subject"],
            message=strip_tags(email["message"].replace("</p>", "</p>\n")),
            from_email=email["from_email"],
            recipient_list=[ea.strip() for ea in email["recipient_list"].split(",")],
            html_message=email["message"],
            reply_to=[ea.strip() for ea in email["reply_to"].split(",")],
        )

    class Meta:  # type: ignore
        abstract = True
