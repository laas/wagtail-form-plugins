"""Models definition for the File Input form plugin."""

import uuid
from datetime import date, datetime, time, timezone
from pathlib import Path

from django.conf import settings
from django.db import models
from django.forms import BaseForm

from wagtail_form_plugins.streamfield.dicts import SubmissionData
from wagtail_form_plugins.streamfield.forms import StreamFieldFormField
from wagtail_form_plugins.streamfield.models import StreamFieldFormPage

from .views import FileInputSubmissionsListView

from typing_extensions import Self


class AbstractFileInput(models.Model):
    """The file input model class, containing several Django fields such as the file field."""

    file = models.FileField()
    field_name = models.CharField(blank=True, max_length=254)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.upload_dir = ""
        self.file.field.upload_to = self.get_file_path

    def __str__(self) -> str:
        """Pretty prints the FileInput object for convenience."""
        return f"{self.field_name}: {self.file.name if self.file else '-'}"

    def get_file_path(self, _instance: Self, file_name: str) -> Path:
        """Get the path of the uploaded file."""
        file_path = Path(file_name)
        dir_path = Path(datetime.now(tz=timezone.utc).strftime(str(self.upload_dir)))
        new_file_name = f"{file_path.stem}_{uuid.uuid4()}{file_path.suffix}"
        return dir_path / new_file_name


class DefaultFileInput(AbstractFileInput):
    """Default file input doing nothing more than the AbstractFileInput except it's not abstract."""


class FileInputFormPage(StreamFieldFormPage):
    """Form page for the FileInput plugin, used for instance to get the file url in submission."""

    submissions_list_view_class = FileInputSubmissionsListView
    file_input_upload_dir = "forms_uploads/%Y/%m/%d"
    file_input_class = DefaultFileInput

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        submission_data = super().pre_process_form_submission(form)

        form_fields = self.get_form_fields_dict()
        for field_slug, field_value in submission_data["form_data"].items():
            form_field = form_fields[field_slug]
            if form_field.type == "file":
                file_input = self.file_input_class.objects.create(
                    file=field_value,
                    field_name=field_slug,
                )
                file_input.upload_dir = self.file_input_upload_dir
                file_url = file_input.file.url if file_input.file else ""
                submission_data["form_data"][field_slug] = file_url

        return submission_data

    def format_field_value(
        self,
        form_field: StreamFieldFormField,
        value: str | list | date | time | datetime | None,
        *,
        in_html: bool,
    ) -> str | None:
        """Format the field value. Used to display user-friendly values in result table."""
        fmt_value = super().format_field_value(form_field, value, in_html=in_html)

        if form_field.type == "file":
            return (settings.WAGTAILADMIN_BASE_URL + fmt_value) if value else None

        return fmt_value

    class Meta:
        abstract = True
