"""View classes for the plugins."""

from collections import OrderedDict
from datetime import datetime
from typing import Any

from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView

from .dicts import SubmissionContextData
from .models import StreamFieldFormPage


class StreamFieldSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    def get_header(self, context_data: SubmissionContextData) -> list[str]:
        """Return slugs of context data header entries."""
        return [head["name"] for head in context_data["data_headings"]]

    def get_submissions(self, context_data: SubmissionContextData) -> dict[str, FormSubmission]:
        """Return a dictionnary containing context data submissions."""
        return {s.pk: s for s in context_data["submissions"]}

    def to_row_dict(self, item: FormSubmission) -> dict[str, Any]:
        """Convert a form submission to a dict, overrided to format cells."""
        row_dict = super().to_row_dict(item)
        return self.format_row_dict(item, row_dict, in_html=False)

    def format_row_dict(
        self, submission: FormSubmission, row_dict: dict[str, Any], *, in_html: bool
    ) -> dict:
        """Format row cells for both csv/xslx exports and web table."""
        fields = self.form_page.get_form_fields_dict()

        for cell_key, cell_value in row_dict.items():
            if cell_key in fields:
                fmt_value = self.form_page.format_field_value(
                    fields[cell_key], submission.form_data.get(cell_key, None), in_html=in_html
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
        submissions = self.get_submissions(context_data)

        for row_idx, row in enumerate(context_data["data_rows"]):
            submission = submissions[row["model_id"]]
            row_items = [
                (header[col_idx], context_data["data_rows"][row_idx]["fields"][col_idx])
                for col_idx, col_value in enumerate(row["fields"])
            ]
            row_dict = self.format_row_dict(submission, OrderedDict(row_items), in_html=True)

            for cell_idx, cell_value in enumerate(row_dict.values()):
                context_data["data_rows"][row_idx]["fields"][cell_idx] = cell_value

        return context_data
