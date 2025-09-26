"""View classes for the Conditional Fields plugin."""

from typing import Any

from wagtail_form_plugins.base import BaseSubmissionsListView


class ConditionalFieldsSubmissionsListView(BaseSubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Return context for view"""
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        for row_idx, row in enumerate(context_data["data_rows"]):
            context_data["data_rows"][row_idx]["fields"] = [
                "-" if val is None else val for val in row["fields"]
            ]

        return context_data
