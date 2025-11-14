"""Models definition for the Token Validation form plugin."""

import base64
import uuid
from datetime import datetime, timezone
from typing import Any, ClassVar

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.forms import BaseForm, EmailField, Form
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField

from wagtail_form_plugins.streamfield.dicts import SubmissionData
from wagtail_form_plugins.streamfield.models import StreamFieldFormPage, StreamFieldFormSubmission
from wagtail_form_plugins.utils import build_email


class ValidationForm(Form):
    """A small form with an email field, used to send validation email to access the actual form."""

    validation_email = EmailField(
        max_length=100,
        help_text=_("An e-mail validation is required to fill public forms when not connected."),
    )


class ValidationFormSubmission(StreamFieldFormSubmission):
    """A mixin used to update the email value in the submission."""

    email = models.EmailField(default="")

    def get_data(self) -> dict[str, Any]:
        """Return dict with form data."""
        data = super().get_data()
        if not data.get("email", None):
            data["email"] = self.email
        return data

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        abstract = True


class ValidationFormPage(StreamFieldFormPage):
    """A mixin used to add validation functionnality to a form."""

    token_validation_form_class = ValidationForm
    token_validation_title_field_name = "validation_title"  # noqa: S105
    token_validation_body_field_name = "validation_body"  # noqa: S105
    token_validation_from_email = ""
    token_validation_reply_to: ClassVar = []
    token_validation_expiration_delay = 60

    validation_title = models.CharField(
        verbose_name=_("E-mail title"),
        default=_("User validation required to fill a public form"),
        max_length=100,
    )
    validation_body = RichTextField(
        verbose_name=_("E-mail content"),
        default=_("Please click on the following link to fill the form: {validation_url} ."),
    )

    def __init__(self, *args, **kwargs):
        self.tokens: dict[str, datetime] = {}
        super().__init__(*args, **kwargs)

    def build_token(self, email: str) -> str:
        """Generate and return the token used to validate the form."""
        encoded_email = base64.b64encode(email.encode("utf-8")).decode("utf-8")
        return f"{encoded_email}-{uuid.uuid4()}"

    def flush(self) -> None:
        """Remove the expired tokens."""
        to_remove = []
        for token, date in self.tokens.items():
            delay = datetime.now(timezone.utc) - date
            if delay.total_seconds() / 60 > self.token_validation_expiration_delay:
                to_remove.append(token)

        for token in to_remove:
            del self.tokens[token]

    def extract_email(self, form: BaseForm) -> str:
        """Extract the email encoded in the token."""
        encoded_email: str = form.data["wfp_token"].split("-")[0]
        return base64.b64decode(encoded_email.encode("utf-8")).decode("utf-8")

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        submission_data = super().pre_process_form_submission(form)

        submission_data["email"] = self.extract_email(form)  # type: ignore[invalid-key]

        return submission_data

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)
        self.flush()

        if not request.user.is_anonymous:
            return response

        if request.method == "POST":
            if "validation_email" in request.POST:
                form = self.token_validation_form_class(request.POST)
                if form.is_valid():
                    validation_email = form.cleaned_data["validation_email"]
                    token = self.build_token(validation_email)
                    self.tokens[token] = datetime.now(timezone.utc)

                    email = self.build_validation_email(validation_email, token)
                    self.send_validation_email(email)

                    msg_str = _(
                        "We just send you an e-mail. Please click on the link to continue the form submission.",  # noqa: E501
                    )
                    messages.add_message(request, messages.INFO, msg_str)
                else:
                    messages.add_message(request, messages.ERROR, _("This e-mail is not valid."))
            elif "wfp_token" in request.POST and request.POST["wfp_token"] in self.tokens:
                del self.tokens[request.POST["wfp_token"]]
                return response

        if request.method == "GET" and "token" in request.GET:
            token = request.GET["token"]
            if token in self.tokens:
                msg_str = _("Your e-mail has been validated. You can now fill the form.")
                messages.add_message(request, messages.SUCCESS, msg_str)

                return response
            messages.add_message(request, messages.ERROR, _("This token is not valid."))

        context = self.get_context(request)
        context["form"] = self.token_validation_form_class()
        return TemplateResponse(request, self.get_template(request), context)

    def process_form_submission(self, form: BaseForm) -> StreamFieldFormSubmission:
        """Create and return submission instance. Update email value."""
        submission = super().process_form_submission(form)
        submission.email = self.extract_email(form)  # type: ignore[unresolved-attribute]
        return submission

    def build_validation_email(self, email_address: str, token: str) -> EmailMultiAlternatives:
        """Send an e-mail containing the link used to validate the form."""
        validation_url = f"{settings.WAGTAILADMIN_BASE_URL}{self.url}?token={token}"
        validation_body = getattr(self, self.token_validation_body_field_name)

        message_text = validation_body.replace("{validation_url}", validation_url)
        message_html = validation_body.replace(
            "{validation_url}",
            f"<a href='{validation_url}'>{validation_url}</a>",
        )
        return build_email(
            subject=getattr(self, self.token_validation_title_field_name),
            message=message_text,
            from_email=self.token_validation_from_email,
            recipient_list=email_address,
            html_message=message_html,
            reply_to=self.token_validation_reply_to,
        )

    def send_validation_email(self, email: EmailMultiAlternatives) -> None:
        """Send the validation e-mail."""
        email.send()

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        abstract = True
