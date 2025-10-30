"""Models definition for the Emails form plugin."""

from typing import Any

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage
from wagtail_form_plugins.utils import build_email

from .dicts import EmailsToSendBlockDict


class EmailActionsFormPage(StreamFieldFormPage):
    """Form page for the EmailActions plugin, allowing to send emails when submitting a form."""

    emails_field_attr_name = "emails_to_send"

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        context = self.get_context(request)

        if "form_submission" in context:
            form_page: StreamFieldFormPage = context["page"]

            fmt_class = getattr(self, "templating_formatter_class", None)
            text_formatter = fmt_class(context, False) if fmt_class else None
            html_formatter = fmt_class(context, True) if fmt_class else None

            for email in getattr(form_page, self.emails_field_attr_name, []):
                email = self.build_action_email(email.value, text_formatter, html_formatter)
                self.send_action_email(email)

        return super().serve(request, *args, **kwargs)

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
