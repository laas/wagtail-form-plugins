from django.utils.html import format_html
from django.conf import settings

from wagtail.contrib.forms.views import SubmissionsListView


class FileInputSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        fields_slug = [head["name"] for head in context_data["data_headings"]]
        fields_type = {f.clean_name: f.field_type for f in self.form_page.get_form_fields()}

        for row_idx, row in enumerate(context_data["data_rows"]):
            for col_idx, value in enumerate(row["fields"]):
                field_slug = fields_slug[col_idx]
                if field_slug in fields_type and fields_type[field_slug] == "file":
                    file_link = self.get_file_link(value, True)
                    context_data["data_rows"][row_idx]["fields"][col_idx] = file_link

        return context_data

    @staticmethod
    def get_file_link(file_url, to_html):
        if not file_url:
            return "-"

        full_url = settings.WAGTAILADMIN_BASE_URL + file_url
        html_template = "<a href='{url}' target='_blank'>download</a>"
        return format_html(html_template, url=full_url) if to_html else full_url
