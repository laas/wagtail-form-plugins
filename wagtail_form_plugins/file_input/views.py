from django.utils.html import format_html
from django.conf import settings

from wagtail.contrib.forms.views import SubmissionsListView


class FileInputSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        fields_slug = [head["name"] for head in context["data_headings"]]
        fields_type = {f.clean_name: f.field_type for f in self.form_page.get_form_fields()}

        for row_idx, row in enumerate(context["data_rows"]):
            for col_idx, val in enumerate(row["fields"]):
                field_slug = fields_slug[col_idx]
                if field_slug in fields_type and fields_type[field_slug] == "file":
                    context["data_rows"][row_idx]["fields"][col_idx] = self.get_file_link(val, True)

        return context

    @staticmethod
    def get_file_link(file_url, to_html):
        if not file_url:
            return "-"

        full_url = settings.WAGTAILADMIN_BASE_URL + file_url
        html_template = "<a href='{url}' target='_blank'>download</a>"
        return format_html(html_template, url=full_url) if to_html else full_url
