"""View classes for the Conditional Fields plugin."""

from typing import Any

from wagtail_form_plugins.streamfield.views import StreamFieldSubmissionsListView


class LabelSubmissionsListView(StreamFieldSubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Alter submission context data to don't show label fields."""
        ctx_data = super().get_context_data(**kwargs)

        header: list[str] = [head["name"] for head in ctx_data["data_headings"]]
        fields = self.form_page.get_form_fields_dict()

        def show_column(col_idx: int) -> bool:
            field = fields.get(header[col_idx], None)
            return field is None or field.type != "label"

        ctx_data["data_headings"] = [
            h
            for h in ctx_data["data_headings"]
            if h["name"] not in fields or fields[h["name"]].type != "label"
        ]

        for row_idx, row in enumerate(ctx_data["data_rows"]):
            ctx_data["data_rows"][row_idx]["fields"] = [
                col for col_idx, col in enumerate(row["fields"]) if show_column(col_idx)
            ]

        return ctx_data
