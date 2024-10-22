from pathlib import Path

from django import forms
from django.utils.html import format_html

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.views import SubmissionsListView

from wagtail_form_mixins.base.models import PluginBase


class FileInputFormBuilder(FormBuilder):
    def create_file_field(self, field_value, options):
        return forms.FileField(**options)


class FileInputSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            field_types = [
                "user",
                "submission_date",
                *(field_data["type"] for field_data in self.form_page.get_form_fields().raw_data),
            ]
            data_rows = context["data_rows"]

            for data_row in data_rows:
                fields = data_row["fields"]

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == "file" and value:
                        file = self.form_page.file_input_model.objects.get(pk=value)

                        fields[idx] = format_html(
                            "<a href='{}' target='_blank'>{}</a>",
                            file.file.url,
                            Path(file.file.name).name,
                        )

        return context


class FileInputFormMixin(PluginBase):
    submissions_list_view_class = FileInputSubmissionsListView

    def get_submission_options(self, form):
        file_form_fields = [
            get_field_clean_name(field_data["value"]["label"])
            for field_data in self.get_form_fields().raw_data
            if field_data["type"] == "file"
        ]

        for field_name, field_value in form.cleaned_data.items():
            if field_name in file_form_fields:
                uploaded_file = self.file_input_model.objects.create(
                    file=field_value, field_name=field_name
                )

                form.cleaned_data[field_name] = uploaded_file.pk

        return {
            **super().get_submission_options(form),
            "form_data": form.cleaned_data,
        }

    class Meta:
        abstract = True
