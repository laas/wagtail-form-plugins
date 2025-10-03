"""Models definition for the Emails form plugin."""

from typing import Any

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield import StreamFieldFormPage
from wagtail_form_plugins.utils import build_email


class EmailActionsFormPage(StreamFieldFormPage):
    """Form page for the EmailActions plugin, allowing to send emails when submitting a form."""

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        if "form_submission" in response.context_data:
            form_page: StreamFieldFormPage = response.context_data["page"]
            for email in form_page.emails_to_send:  # type: ignore
                email = self.build_action_email(email.value)
                self.send_action_email(email)

        return response

    def build_action_email(self, email_value: dict[str, Any]) -> EmailMultiAlternatives:
        return build_email(
            subject=email_value["subject"],
            message=email_value["message"],
            from_email=email_value["from_email"],
            recipient_list=email_value["recipient_list"],
            html_message=email_value["message"],
            reply_to=email_value["reply_to"],
        )

    def send_action_email(self, email: EmailMultiAlternatives) -> None:
        """Send an e-mail"""
        email.send()

    class Meta:  # type: ignore
        abstract = True
