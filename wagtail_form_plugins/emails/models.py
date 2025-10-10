"""Models definition for the Emails form plugin."""

from typing import Any

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield import StreamFieldFormPage
from wagtail_form_plugins.utils import build_email

from .utils import EmailsToSendBlockDict


class EmailActionsFormPage(StreamFieldFormPage):
    """Form page for the EmailActions plugin, allowing to send emails when submitting a form."""

    emails_field_attr_name = "emails_to_send"

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        if "form_submission" in response.context_data:
            form_page: StreamFieldFormPage = response.context_data["page"]

            fmt_class = getattr(self, "templating_formatter_class", None)
            text_formatter = fmt_class(response.context_data, False) if fmt_class else None
            html_formatter = fmt_class(response.context_data, True) if fmt_class else None

            for email in getattr(form_page, self.emails_field_attr_name, []):
                email = self.build_action_email(email.value, text_formatter, html_formatter)
                self.send_action_email(email)

        return response

    def build_action_email(
        self, email_value: EmailsToSendBlockDict, text_formatter: Any, html_formatter: Any
    ) -> EmailMultiAlternatives:
        def format_text(text: str) -> str:
            return text_formatter.format(text) if text_formatter else text

        def format_html(text: str) -> str:
            return html_formatter.format(text) if html_formatter else text.replace("\n", "<br/>")

        return build_email(
            subject=format_text(email_value["subject"]),
            message=format_text(str(email_value["message"])),
            from_email=email_value["from_email"],
            recipient_list=format_text(email_value["recipient_list"]),
            reply_to=email_value["reply_to"],
            html_message=format_html(str(email_value["message"])),
        )

    def send_action_email(self, email: EmailMultiAlternatives) -> None:
        """Send an e-mail"""
        email.send()

    class Meta:  # type: ignore
        abstract = True
