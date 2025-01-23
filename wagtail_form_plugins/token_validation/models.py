import uuid
import base64

from datetime import datetime, timezone

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.response import TemplateResponse
from django.forms import Form, EmailField
from django.contrib import messages
from django.utils.html import strip_tags
from django.db import models
from django.http import HttpRequest

from wagtail_form_plugins.base.models import FormMixin
from wagtail.contrib.forms.models import AbstractFormSubmission


class ValidationForm(Form):
    validation_email = EmailField(
        max_length=100,
        help_text=_("An e-mail validation is required to fill public forms when not connected."),
    )


class TokenValidationSubmission(AbstractFormSubmission):
    email = models.EmailField(default="")

    def get_data(self):
        return {
            **super().get_data(),
            "email": self.email,
        }

    class Meta:
        abstract = True


class TokenValidationFormMixin(FormMixin):
    tokens: dict[str, datetime] = {}

    def build_token(self, email: str) -> str:
        encoded_email = base64.b64encode(email.encode("utf-8")).decode("utf-8")
        return f"{ encoded_email }-{uuid.uuid4()}"

    def flush(self):
        for token, date in self.tokens.items():
            delay = datetime.now(timezone.utc) - date
            if delay.total_seconds() / 60 > settings.FORMS_VALIDATION_EXPIRATION_DELAY:
                del self.tokens[token]

    def get_data_fields(self):
        return [
            ("email", _("Validation email")),
            *super().get_data_fields(),
        ]

    def get_submission_options(self, form):
        encoded_email: str = form.data["wfp_token"].split("-")[0]
        email = base64.b64decode(encoded_email.encode("utf-8")).decode("utf-8")
        return {
            **super().get_submission_options(form),
            "email": email,
        }

    def serve(self, request: HttpRequest, *args, **kwargs):
        self.flush()

        if not request.user.is_anonymous:
            return super().serve(request, *args, **kwargs)

        if request.method == "POST":
            if "validation_email" in request.POST:
                form = ValidationForm(request.POST)
                if form.is_valid():
                    validation_email = form.cleaned_data["validation_email"]
                    token = self.build_token(validation_email)
                    self.tokens[token] = datetime.now(timezone.utc)
                    self.send_validation_email(validation_email, token)
                    msg_str = _(
                        "We just send you an e-mail. Please click on the link to continue the form submission."
                    )
                    messages.add_message(request, messages.INFO, msg_str)
                else:
                    messages.add_message(request, messages.ERROR, _("This e-mail is not valid."))
            elif "wfp_token" in request.POST and request.POST["wfp_token"] in self.tokens:
                del self.tokens[request.POST["wfp_token"]]
                return super().serve(request, *args, **kwargs)

        if request.method == "GET" and "token" in request.GET:
            token = request.GET["token"]
            if token in self.tokens:
                msg_str = _("Your e-mail has been validated. You can now fill the form.")
                messages.add_message(request, messages.SUCCESS, msg_str)

                return super().serve(request, *args, **kwargs)
            messages.add_message(request, messages.ERROR, _("This token is not valid."))

        context = self.get_context(request)
        context["form"] = ValidationForm()
        return TemplateResponse(request, self.get_template(request), context)

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        submission.email = f"{form.data['wfp_token']}@laas.fr"
        return submission

    def send_validation_email(self, email_address: str, token: str):
        validation_url = f"{settings.WAGTAILADMIN_BASE_URL}{ self.url }?token={ token }"
        message_text = self.validation_body.replace(
            "{validation_url}",
            validation_url,
        )
        message_html = self.validation_body.replace(
            "{validation_url}",
            f"<a href='{ validation_url }'>{ validation_url }</a>",
        )
        email = {
            "subject": self.validation_title,
            "recipient_list": [email_address],
            "from_email": settings.FORMS_FROM_EMAIL,
            "message": strip_tags(message_text.replace("</p>", "</p>\n")),
            "html_message": message_html,
        }
        self.send_email(email)

    class Meta:
        abstract = True
