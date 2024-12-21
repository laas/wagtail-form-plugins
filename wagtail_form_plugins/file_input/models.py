import uuid
from pathlib import Path
from datetime import datetime

from typing import Any
from django.conf import settings
from django.db import models

from wagtail_form_plugins.base.models import FormMixin
from wagtail_form_plugins.file_input.views import FileInputSubmissionsListView


class AbstractFileInput(models.Model):
    file = models.FileField()
    field_name = models.CharField(blank=True, max_length=254)
    upload_dir = "forms_uploads/%Y/%m/%d"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.file.field.upload_to = self.get_file_path

    def get_file_path(self, instance, file_name):
        file_path = Path(file_name)
        dir_path = Path(datetime.now().strftime(str(self.upload_dir)))
        new_file_name = f"{ file_path.stem }_{ uuid.uuid4() }{ file_path.suffix }"
        return dir_path / new_file_name

    def __str__(self) -> str:
        return f"{self.field_name}: {self.file.name if self.file else '-'}"

    class Meta:
        abstract = True


class FileInputFormMixin(FormMixin):
    submissions_list_view_class = FileInputSubmissionsListView

    def get_submission_options(self, form):
        file_form_fields = [f.clean_name for f in self.get_form_fields() if f.field_type == "file"]

        for field_name, field_value in form.cleaned_data.items():
            if field_name in file_form_fields:
                file_input = self.file_input_model.objects.create(
                    file=field_value, field_name=field_name
                )
                form.cleaned_data[field_name] = file_input.file.url if file_input.file else ""

        return {
            **super().get_submission_options(form),
            "form_data": form.cleaned_data,
        }

    def format_field_value(self, field_type, field_value):
        fmt_value = super().format_field_value(field_type, field_value)

        if field_type == "file":
            return (settings.WAGTAILADMIN_BASE_URL + fmt_value) if field_value else "-"

        return fmt_value

    class Meta:
        abstract = True
