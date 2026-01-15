"""Models definition for the Emails form plugin."""

from typing import TYPE_CHECKING

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield.models import (
    StreamFieldFormatter,
    StreamFieldFormPage,
    StreamFieldFormSubmission,
)
from wagtail_form_plugins.utils import build_email, multiline_to_html

from .dicts import EmailsToSendBlockDict

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class EmailActionsFormPage(StreamFieldFormPage):
    """Form page for the EmailActions plugin, allowing to send emails when submitting a form."""

    emails_field_attr_name = "emails_to_send"

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)

        if (
            isinstance(response, HttpResponseRedirect)
            or not response.context_data
            or (request.method == "POST" and "edit" in request.POST)
        ):
            return response

        if "form_submission" in response.context_data:
            form_page: StreamFieldFormPage = response.context_data["page"]

            if hasattr(self, "templating_formatter_class"):
                fmt_class: type[StreamFieldFormatter] = self.templating_formatter_class  # ty: ignore invalid-assignment
                form_page: StreamFieldFormPage = response.context_data["page"]
                user: User = request.user  # ty: ignore invalid-assignment
                form_submis: StreamFieldFormSubmission = response.context_data["form_submission"]
                text_formatter = fmt_class(form_page, user, form_submis, in_html=False)
                html_formatter = fmt_class(form_page, user, form_submis, in_html=True)
            else:
                text_formatter = None
                html_formatter = None

            for raw_email in getattr(form_page, self.emails_field_attr_name, []):
                email = self.build_action_email(raw_email.value, text_formatter, html_formatter)
                self.send_action_email(email)

        return response

    def build_action_email(
        self,
        email_value: EmailsToSendBlockDict,
        text_formatter: StreamFieldFormatter | None,
        html_formatter: StreamFieldFormatter | None,
    ) -> EmailMultiAlternatives:
        """Build the action email based on the value in an email form block."""

        def format_text(text: str) -> str:
            return text_formatter.format(text) if text_formatter else text

        def format_html(text: str) -> str:
            return html_formatter.format(text) if html_formatter else multiline_to_html(text)

        return build_email(
            subject=format_text(email_value["subject"]),
            message=format_text(str(email_value["message"])),
            from_email=format_text(email_value["from_email"]),
            recipient_list=format_text(email_value["recipient_list"]),
            reply_to=format_text(email_value["reply_to"]),
            html_message=format_html(str(email_value["message"])),
        )

    def send_action_email(self, email: EmailMultiAlternatives) -> None:
        """Send an e-mail. Can be overrided to change behaviour."""
        email.send()

    class Meta:
        abstract = True
