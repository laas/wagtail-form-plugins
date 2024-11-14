from django.utils.html import format_html
from django.conf import settings

from wagtail.contrib.forms.views import SubmissionsListView


class FileInputSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            field_types = [
                "index",
                "user",
                "submission_date",
                *(field.field_type for field in self.form_page.get_form_fields()),
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
