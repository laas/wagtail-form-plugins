from django import forms
from django.utils.html import format_html
from django.conf import settings

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.views import SubmissionsListView

from wagtail_form_mixins.base.models import FormMixin


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
                    if field_type == "file":
                        fields[idx] = FileInputSubmissionsListView.get_file_link(value, True)

        return context

    @staticmethod
    def get_file_link(file_url, to_html):
        if not file_url:
            return "-"

        full_url = settings.WAGTAILADMIN_BASE_URL + file_url
        html_template = "<a href='{url}' target='_blank'>download</a>"
        return format_html(html_template, url=full_url) if to_html else full_url


class FileInputFormMixin(FormMixin):
    submissions_list_view_class = FileInputSubmissionsListView

    def get_submission_options(self, form):
        file_form_fields = [
            get_field_clean_name(field_data["value"]["label"])
            for field_data in self.get_form_fields().raw_data
            if field_data["type"] == "file"
        ]

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
