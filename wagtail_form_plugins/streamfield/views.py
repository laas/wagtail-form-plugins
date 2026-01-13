"""View classes for the plugins."""

from datetime import datetime

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

    def get_context_data(self, **kwargs) -> SubmissionContextData:  # type: ignore reportAssignmentType
        """Alter submission context data to format results."""
        context_data: SubmissionContextData = super().get_context_data(**kwargs)  # type: ignore reportAssignmentType

        if self.is_export:
            return context_data

        header = self.get_header(context_data)
        fields = self.form_page.get_form_fields_dict()
        submissions = self.get_submissions(context_data)

        for row_idx, row in enumerate(context_data["data_rows"]):
            submission = submissions[row["model_id"]]
            for col_idx, col_value in enumerate(row["fields"]):
                field_header = header[col_idx]
                if field_header in fields:
                    fmt_value = self.form_page.format_field_value(
                        fields[field_header],
                        submission.form_data.get(field_header, None),
                        in_html=True,
                    )
                elif field_header == "submit_time" and isinstance(col_value, datetime):
                    fmt_value = col_value.strftime("%d/%m/%Y, %H:%M")
                else:
                    fmt_value = col_value

                context_data["data_rows"][row_idx]["fields"][col_idx] = fmt_value or "-"

        return context_data
