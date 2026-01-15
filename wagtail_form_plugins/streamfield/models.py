"""Models definition for the Streamfield form plugin."""

from datetime import date, datetime, time
from typing import Any

from django.contrib.auth.models import User
from django.forms import BaseForm
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.utils.html import format_html

from wagtail.admin.panels import RichText
from wagtail.contrib.forms.models import AbstractFormSubmission, FormMixin
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.models import Page

from wagtail_form_plugins.utils import create_links, format_list, multiline_to_html

from .dicts import SubmissionData
from .forms import StreamFieldFormBuilder, StreamFieldFormField


class StreamFieldFormSubmission(AbstractFormSubmission):
    """A custom form submission class used for StreamField forms."""

    class Meta:
        abstract = True


class StreamFieldFormPage(FormMixin, Page):
    """Base form page that will be extended with plugins."""

    form_builder_class = StreamFieldFormBuilder
    form_submission_class = StreamFieldFormSubmission
    form_field_class = StreamFieldFormField
    submissions_list_view_class = SubmissionsListView

    fields_field_attr_name = "form_fields"

    @property
    def form_builder(self) -> type[StreamFieldFormBuilder]:
        """Return form builder class (used in wagtail.FormMixin): alias for form_builder_class."""
        return self.form_builder_class

    def get_submission_class(self) -> type[StreamFieldFormSubmission]:
        """Return for submission class. Used in wagtail.FormMixin."""
        return self.form_submission_class

    def serve_preview(self, request: HttpRequest, mode_name: str) -> TemplateResponse | None:
        """Fix typing: FormMixin.serve_preview and Page.serve_preview return types are different."""
        return super().serve_preview(request, mode_name)

    def get_form_fields(self) -> list[StreamFieldFormField]:
        """Return the form fields based on streamfield data."""
        steamchild = getattr(self, self.fields_field_attr_name)
        return [
            self.form_field_class.from_streamfield_data(field_data)
            for field_data in steamchild.raw_data
        ]

    def get_form_fields_dict(self) -> dict[str, StreamFieldFormField]:
        """Return a field_slug:field dictionnary of all form fields."""
        return {field.slug: field for field in self.get_form_fields()}

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        """Return a list of slugs corresponding to enabled fields (usually via a condition)."""
        return [slug for slug, field_data in form_data.items() if field_data is not None]

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Pre-processing step before to create the form submission object."""
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def process_form_submission(self, form: BaseForm) -> StreamFieldFormSubmission:
        """
        Create and return the submission instance.

        This does not call the super method in order to call pre_process_form_submission before
        instantiating the submission object.
        """
        submission_data = self.pre_process_form_submission(form)
        return self.form_submission_class.objects.create(**submission_data)

    def format_field_value(  # noqa: C901, PLR0912
        self,
        form_field: StreamFieldFormField,
        value: str | list | date | time | datetime | None,
        *,
        in_html: bool,
    ) -> str | None:
        """
        Format the field value, or return None if the value should not be displayed.

        Used to display user-friendly values in result table and emails.
        """
        fmt_value = value

        if value is None:
            fmt_value = None

        elif form_field.type in ["checkboxes", "multiselect"] and isinstance(value, list):
            fmt_value = format_list(
                [v for k, v in form_field.choices if k in value],
                "  •",
                in_html=in_html,
            )

        elif form_field.type in ["dropdown", "radio"] and isinstance(value, str):
            fmt_value = dict(form_field.choices).get(value, "-")

        elif form_field.type == "multiline" and isinstance(value, str):
            fmt_value = (
                format_html("<br/>{value}", value=multiline_to_html(value))
                if in_html
                else f"\n{value.strip()}"
            )

        elif form_field.type == "datetime":
            if isinstance(value, str):
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if isinstance(value, datetime):
                fmt_value = value.strftime("%d/%m/%Y, %H:%M")

        elif form_field.type == "date":
            if isinstance(value, str):
                value = date.fromisoformat(value)
            if isinstance(value, date):
                fmt_value = value.strftime("%d/%m/%Y")

        elif form_field.type == "time":
            if isinstance(value, str):
                value = time.fromisoformat(value)
            if isinstance(value, time):
                fmt_value = value.strftime("%H:%M")

        elif form_field.type == "number":
            fmt_value = str(value)

        elif form_field.type == "checkbox":
            fmt_value = "✔" if value else "✘"

        if not isinstance(fmt_value, str | None):
            msg = f"col_value '{fmt_value}' is of type {type(fmt_value)} instead of str or None."
            raise TypeError(msg)

        return fmt_value

    def get_form(self, *args, page: "StreamFieldFormPage", user: User, **kwargs) -> BaseForm:
        """Build and return the form instance."""
        form = super().get_form(*args, page=page, user=user, **kwargs)

        form_fields = self.get_form_fields_dict()

        for field_slug, field_value in form.fields.items():
            form_field = form_fields[field_slug]
            field_value.widget.attrs["id"] = form_field.block_id
            field_value.widget.attrs["data-label"] = form_field.label
            field_value.widget.attrs["data-type"] = form_field.type

            if field_value.help_text:
                field_value.help_text = create_links(str(field_value.help_text)).replace("\n", "")

        if args:
            form.full_clean()

            for k, v in form_fields.items():
                if k not in form.cleaned_data and v.field_type in ["radio", "checkboxes"]:
                    form.cleaned_data[k] = None

            enabled_fields = self.get_enabled_fields(form.cleaned_data)
            for field_value in form.fields.values():
                if field_value.widget.attrs.get("data-slug", None) not in enabled_fields:
                    field_value.required = False

        form.full_clean()
        return form

    class Meta:
        abstract = True


class StreamFieldFormatter:
    """Class used as an interface for TemplatingFormatter."""

    def __init__(
        self,
        form_page: StreamFieldFormPage,
        user: User,
        submission: StreamFieldFormSubmission | None = None,
        *,
        in_html: bool = False,
    ) -> None:
        self.submission = submission
        self.form_page = form_page
        self.user = user
        self.in_html = in_html

    def format(self, message: str | RichText) -> str:
        """Format the given message."""
        raise NotImplementedError
