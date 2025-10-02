"""View classes for the Conditional Fields plugin."""

from datetime import date, time, datetime
from typing import Any

from wagtail.contrib.forms.views import SubmissionsListView

from . import StreamFieldFormPage


class StreamFieldSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    # def format_field(col_idx: int, field_value: Any):
    #     field_slug = fields_slug[col_idx]
    #     if field_slug == "submit_time":
    #         return field_value.strftime("%d/%m/%Y, %H:%M")
    #     if field_slug in fields:
    #         return value
    #     return field_value

    # if field.choices:
    #     new_submission_data[data_key] = ",".join(post.getlist(data_key))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Return context for view"""
        context_data = super().get_context_data(**kwargs)
        print("=== StreamFieldSubmissionsListView.get_context_data ===")
        print("data_rows:", context_data["data_rows"])

        # fields_slug = [head["name"] for head in context_data["data_headings"]]

        for row_idx, row in enumerate(context_data["data_rows"]):
            for col_idx, value in enumerate(row["fields"]):
                # field_slug = fields_slug[col_idx]
                fmt_value = None

                if isinstance(value, datetime):
                    fmt_value = value.strftime("%d/%m/%Y, %H:%M")
                elif isinstance(value, date):
                    fmt_value = value.strftime("%d/%m/%Y")
                elif isinstance(value, time):
                    # TODO: vérifier
                    fmt_value = value.strftime("%H:%M")
                elif isinstance(value, list):
                    fmt_value = ", ".join(value)
                elif value is None:
                    fmt_value = "-"

                if fmt_value:
                    context_data["data_rows"][row_idx]["fields"][col_idx] = fmt_value

        return context_data
