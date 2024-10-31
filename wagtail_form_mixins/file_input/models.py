from django.conf import settings
from django.db import models

from wagtail_form_mixins.base.models import FormMixin
from wagtail_form_mixins.file_input.views import FileInputSubmissionsListView


class AbstractFileInput(models.Model):
    file = models.FileField(upload_to="form_file_input/%Y/%m/%d")
    field_name = models.CharField(blank=True, max_length=254)

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
