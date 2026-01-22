"""View classes for the plugins."""

from collections import OrderedDict
from csv import DictWriter
from datetime import datetime

from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView

from .dicts import SubmissionContextData
from .models import StreamFieldFormPage

from openpyxl.worksheet.worksheet import Worksheet


class StreamFieldSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    def get_header(self, context_data: SubmissionContextData) -> list[str]:
        """Return slugs of context data header entries."""
        return [head["name"] for head in context_data["data_headings"]]

    def get_submissions(self, context_data: SubmissionContextData) -> dict[str, FormSubmission]:
        """Return a dictionnary containing context data submissions."""
        return {s.pk: s for s in context_data["submissions"]}

    def write_csv_row(self, writer: DictWriter, row_dict: OrderedDict) -> OrderedDict:
        """Generate cells to append to the csv worksheet (override)."""
        return super().write_csv_row(writer, self.get_row_dict(row_dict))

    def generate_xlsx_row(
        self, worksheet: Worksheet, row_dict: OrderedDict, date_format: str | None = None
    ) -> OrderedDict:
        """Generate cells to append to the xlsx worksheet (override)."""
        return super().generate_xlsx_row(worksheet, self.get_row_dict(row_dict), date_format)

    def get_row_dict(self, row_dict: dict) -> dict:
        """Format row cells for both csv/xslx exports and web table."""
        fields = self.form_page.get_form_fields_dict()
        for cell_key, cell_value in row_dict.items():
            if cell_key in fields:
                fmt_value = self.form_page.format_field_value(
                    fields[cell_key],
                    cell_value,
                    in_html=True,
                )
            elif cell_key == "submit_time" and isinstance(cell_value, datetime):
                fmt_value = cell_value.strftime("%d/%m/%Y, %H:%M")
            else:
                fmt_value = cell_value

            row_dict[cell_key] = fmt_value or "-"
        return row_dict

    def get_context_data(self, **kwargs) -> SubmissionContextData:  # ty: ignore invalid-method-override
        """Alter submission context data to format results."""
        context_data: SubmissionContextData = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        header = self.get_header(context_data)

        for row_idx, row in enumerate(context_data["data_rows"]):
            row_items = [
                (header[col_idx], context_data["data_rows"][row_idx]["fields"][col_idx])
                for col_idx, col_value in enumerate(row["fields"])
            ]
            row_dict = self.get_row_dict(OrderedDict(row_items))

            for cell_idx, cell_value in enumerate(row_dict.values()):
                context_data["data_rows"][row_idx]["fields"][cell_idx] = cell_value

        return context_data
