"""Models definition for the Streamfield form plugin."""

from datetime import date, datetime, time
from typing import Any

from django.forms import BaseForm
from django.http import HttpRequest

from wagtail.contrib.forms.models import AbstractFormSubmission, FormMixin
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page

from wagtail_form_plugins.utils import create_links

from .forms import StreamFieldFormBuilder, StreamFieldFormField
from .utils import SubmissionData, format_choices


class StreamFieldFormSubmission(AbstractFormSubmission):
    class Meta:  # type: ignore
        abstract = True


class StreamFieldFormPage(FormMixin, Page):
    """Form mixin for the Streamfield plugin."""

    form_builder_class = StreamFieldFormBuilder
    form_submission_class = StreamFieldFormSubmission
    form_field_class = StreamFieldFormField
    submissions_list_view_class = SubmissionsListView

    fields_field_attr_name = "form_fields"

    @classmethod
    @property
    def form_builder(cls) -> type[StreamFieldFormBuilder]:
        return cls.form_builder_class

    def get_submission_class(self) -> type[StreamFieldFormSubmission]:  # type: ignore
        """Used in wagtail.FormMixin."""
        return self.form_submission_class

    def serve_preview(self, request: HttpRequest, mode_name: str) -> Any:
        """Fix typing (FormMixin.serve_preview and Page.serve_preview return types are different)"""
        return

    def get_form_fields(self) -> list[StreamFieldFormField]:
        """Return the form fields based on streamfield data."""
        steamchild = getattr(self, self.fields_field_attr_name)
        return [
            self.form_field_class.from_streamfield_data(field_data)
            for field_data in steamchild.raw_data
        ]

    def get_form_fields_dict(self) -> dict[str, StreamFieldFormField]:
        return {field.slug: field for field in self.get_form_fields()}

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        return [slug for slug, field_data in form_data.items() if field_data is not None]

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Pre-processing step before to create the form submission object."""
        enabled_fields = self.get_enabled_fields(form.cleaned_data)
        form_data = {k: (v if k in enabled_fields else None) for k, v in form.cleaned_data.items()}

        return {
            "form_data": form_data,
            "page": self,
        }

    def process_form_submission(self, form: BaseForm) -> StreamFieldFormSubmission:  # type: ignore
        """Create and return the submission instance."""
        submission_data = self.pre_process_form_submission(form)
        return self.form_submission_class.objects.create(**submission_data)

    def format_field_value(
        self, field: StreamFieldFormField, value: Any, in_html: bool
    ) -> str | list[str] | None:
        """
        Format the field value, or return None if the value should not be displayed.
        Used to display user-friendly values in result table and emails.
        """

        if field.type in ["checkboxes", "dropdown", "multiselect", "radio"]:
            choices = {get_field_clean_name(cv): cv for cv in field.choices.values()}
            values = [choices[v].lstrip("*") for v in value]
            return format_choices(values, in_html)

        if field.type == "datetime":
            if isinstance(value, str):
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value.strftime("%d/%m/%Y, %H:%M")

        if field.type == "date":
            if isinstance(value, str):
                value = date.fromisoformat(value)
            return value.strftime("%d/%m/%Y")

        if field.type == "time":
            if isinstance(value, str):
                value = time.fromisoformat(value)
            return value.strftime("%H:%M")

        if field.type == "number":
            return str(value)

        if field.type == "checkbox":
            return "✔" if value else "✘"

        return value

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        for field_value in form.fields.values():
            if field_value.help_text:
                field_value.help_text = create_links(str(field_value.help_text)).replace("\n", "")

        if args:
            form.full_clean()
            enabled_fields = self.get_enabled_fields(form.cleaned_data)
            for field_value in form.fields.values():
                if field_value.slug not in enabled_fields:  # type: ignore
                    field_value.required = False

        form.full_clean()
        return form

    class Meta:  # type: ignore
        abstract = True
