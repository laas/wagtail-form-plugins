"""View classes for the File Input plugin."""

from typing import Any

from django.conf import settings
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.views import StreamFieldSubmissionsListView


class FileInputSubmissionsListView(StreamFieldSubmissionsListView):
    """Customize lists submissions view, such as adding a link on file fields for each row."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Alter submission context data to display a link to the file."""
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        fields_slug = [head["name"] for head in context_data["data_headings"]]
        fields = self.form_page.get_form_fields()

        for row_idx, row in enumerate(context_data["data_rows"]):
            for col_idx, value in enumerate(row["fields"]):
                field_slug = fields_slug[col_idx]
                if field_slug in fields and fields[field_slug].type == "file":
                    file_link = self.get_file_link(value, to_html=True)
                    context_data["data_rows"][row_idx]["fields"][col_idx] = file_link

        return context_data

    @staticmethod
    def get_file_link(file_url: str, *, to_html: bool) -> str:
        """Build an html link poiting to a file url, or `-` if there is no url."""
        if not file_url:
            return "-"

        full_url = settings.WAGTAILADMIN_BASE_URL + file_url
        html_template = "<a href='{url}' target='_blank'>download</a>"
        return format_html(html_template, url=full_url) if to_html else full_url
