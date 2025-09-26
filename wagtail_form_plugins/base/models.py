"""Base model classes for form plugins."""

from typing import Any

from django.core.mail import EmailAlternative, EmailMultiAlternatives
from django.forms import Form

from wagtail.contrib.forms.models import AbstractFormSubmission, FormMixin, FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page

from wagtail_form_plugins.base.forms import BaseField, BaseFormBuilder


class BaseFormSubmission(AbstractFormSubmission):
    def get_base_class(self) -> type[FormSubmission]:
        error_msg = "FormSubmission should implement get_base_class() method"
        raise NotImplementedError(error_msg)

    class Meta:  # type: ignore
        abstract = True


class BaseFormPage(FormMixin, Page):  # type: ignore
    """Base model class for builder classes."""

    form_builder_class = BaseFormBuilder
    submissions_list_view_class = SubmissionsListView

    def get_form_fields_dict(self) -> dict[str, BaseField]:
        return {field.clean_name: field for field in self.get_form_fields()}

    def get_form_fields(self) -> list[BaseField]:
        """Overrided method of FormMixin.get_form_fields(), used when building the form."""
        raise NotImplementedError

    def get_submission_attributes(self, form: Form) -> dict[str, Any]:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def get_submission_class(self) -> type[FormSubmission]:
        raise NotImplementedError

    def process_form_submission(self, form: Form) -> FormSubmission:
        """Create and return submission instance."""
        submission_attributes = self.get_submission_attributes(form)
        return self.get_submission_class().objects.create(**submission_attributes)

    def format_field_value(self, field_type: str, field_value: Any) -> str:
        """Format the field value. Used to display user-friendly values in result table."""
        return field_value

    def send_mail(
        self,
        subject: str,
        message: str,
        from_email: str,
        recipient_list: list[str],
        html_message: str | None,
        reply_to: list[str] | None,
    ) -> None:
        """Send an e-mail. Override this to change the behavior (ie. print the email instead)."""
        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            alternatives=[EmailAlternative(html_message, "text/html")] if html_message else [],
            reply_to=reply_to,
        )
        mail.send()

    class Meta:  # type: ignore
        abstract = True
