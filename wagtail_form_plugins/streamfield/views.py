"""View classes for the Conditional Fields plugin."""

from typing import Any

from wagtail.contrib.forms.models import AbstractFormSubmission
from wagtail.contrib.forms.views import SubmissionsListView

from . import StreamFieldFormPage


class StreamFieldSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Return context for view"""
        context_data = super().get_context_data(**kwargs)

        submissions = {s.id: s for s in context_data["submissions"]}
        header = [head["name"] for head in context_data["data_headings"]]
        fields = self.form_page.get_form_fields_dict()

        for row_idx, row in enumerate(context_data["data_rows"]):
            submission_id = context_data["data_rows"][row_idx]["model_id"]
            submission: AbstractFormSubmission = submissions[submission_id]
            for col_idx, col_value in enumerate(row["fields"]):
                field_header = header[col_idx]
                if field_header in fields:
                    sub_value = submission.form_data[field_header]
                    fmt_value = self.form_page.format_field_value(fields[field_header], sub_value)
                elif field_header == "submit_time":
                    fmt_value = col_value.strftime("%d/%m/%Y, %H:%M")
                else:
                    fmt_value = col_value

                context_data["data_rows"][row_idx]["fields"][col_idx] = fmt_value or "-"

        return context_data
