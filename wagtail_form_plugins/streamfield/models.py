"""Models definition for the Streamfield form plugin."""

from typing import Any

from django.forms import BaseForm


from django.core.mail import EmailAlternative, EmailMultiAlternatives
from django.forms import Form

from django.http import HttpRequest
from wagtail.contrib.forms.models import AbstractFormSubmission, FormMixin, FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page

from wagtail_form_plugins.utils import create_links
from . import StreamFieldFormBuilder, FormField


class StreamFieldFormSubmission(AbstractFormSubmission):
    def get_base_class(self) -> type[FormSubmission]:
        error_msg = "FormSubmission should implement get_base_class() method"
        raise NotImplementedError(error_msg)

    class Meta:  # type: ignore
        abstract = True


class StreamFieldFormPage(FormMixin, Page):
    """Form mixin for the Streamfield plugin."""

    submissions_list_view_class = SubmissionsListView
    form_builder = StreamFieldFormBuilder
    fields_attr_name = "form_fields"

    def serve_preview(self, request: HttpRequest, mode_name: str) -> Any:
        return

    def get_form_fields_dict(self) -> dict[str, FormField]:
        return {field.clean_name: field for field in self.get_form_fields()}

    def get_submission_attributes(self, form: Form) -> dict[str, Any]:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def get_submission_class(self) -> type[FormSubmission]:
        return FormSubmission

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

    def field_from_streamfield_data(self, field_data: dict[str, Any]) -> FormField:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        base_options = ["slug", "label", "help_text", "is_required", "initial"]

        field_value = field_data["value"]
        return FormField(
            block_id=field_data["id"],
            clean_name=field_value["slug"],
            field_type=field_data["type"],
            label=field_value["label"],
            help_text=field_value["help_text"],
            required=field_value["is_required"],
            default_value=field_value.get("initial", None),
            options={k: v for k, v in field_value.items() if k not in base_options},
        )

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        for field in form.fields.values():
            if field.help_text:
                field.help_text = create_links(str(field.help_text)).replace("\n", "")

        return form

    def get_form_fields(self) -> list[FormField]:
        """Return the form fields based on streamfield data."""
        steamchild = getattr(self, self.fields_attr_name)
        return [self.field_from_streamfield_data(field_data) for field_data in steamchild.raw_data]

    class Meta:  # type: ignore
        abstract = True
