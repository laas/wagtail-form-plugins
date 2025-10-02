"""Models definition for the Streamfield form plugin."""

from typing import Any

from django.core.mail import EmailAlternative, EmailMultiAlternatives
from django.forms import BaseForm
from django.http import HttpRequest

from wagtail.contrib.forms.models import AbstractFormSubmission, FormMixin, FormSubmission
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page

from wagtail_form_plugins.utils import create_links

from . import FormField, StreamFieldFormBuilder


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

    def get_submission_class(self) -> type[FormSubmission]:
        """Used in wagtail.FormMixin."""
        return FormSubmission

    def serve_preview(self, request: HttpRequest, mode_name: str) -> Any:
        return

    def get_form_fields(self) -> list[FormField]:
        """Return the form fields based on streamfield data."""
        steamchild = getattr(self, self.fields_attr_name)
        return [FormField.from_streamfield_data(field_data) for field_data in steamchild.raw_data]

    def get_form_fields_dict(self) -> dict[str, FormField]:
        return {field.slug: field for field in self.get_form_fields()}

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        print("=== get_enabled_fields ===")
        print("form_data:", form_data)
        # TODO: disabled "hidden", and "label" in label module:
        # if field.type in ["hidden", "label"]:
        #     continue
        return [slug for slug, field_data in form_data.items() if field_data is not None]

    def pre_process_form_submission(self, form: BaseForm) -> dict[str, Any]:
        """Pre-processing step before to process the form submission."""
        print("=== pre_process_form_submission ===")
        enabled_fields = self.get_enabled_fields(form.cleaned_data)
        print("=== ===")
        form_data = {k: (v if k in enabled_fields else None) for k, v in form.cleaned_data.items()}

        return {
            "form_data": form_data,
            "page": self,
        }

    def process_form_submission(self, form: BaseForm) -> FormSubmission:
        """Create and return the submission instance."""
        submission_data = self.pre_process_form_submission(form)
        return self.get_submission_class().objects.create(**submission_data)

    def format_field_value(self, field: FormField, field_value: Any) -> str | None:
        """
        Format the field value, or return None if the value should not be displayed.
        Used to display user-friendly values in result table.
        """
        if field.type in ["checkboxes", "dropdown", "multiselect", "radio"]:
            choices = {get_field_clean_name(c): c for c in field.choices}
            return ", ".join([choices[v].lstrip("*") for v in field_value.split(",")])

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
        # TODO: Remove. not related to StreamFieldFormPage.
        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            alternatives=[EmailAlternative(html_message, "text/html")] if html_message else [],
            reply_to=reply_to,
        )
        mail.send()

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        for field in form.fields.values():
            if field.help_text:
                field.help_text = create_links(str(field.help_text)).replace("\n", "")

        return form

    class Meta:  # type: ignore
        abstract = True
