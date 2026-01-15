"""View classes for the Conditional Fields plugin."""

from wagtail_form_plugins.streamfield.dicts import SubmissionContextData
from wagtail_form_plugins.streamfield.views import StreamFieldSubmissionsListView


class LabelSubmissionsListView(StreamFieldSubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    def get_context_data(self, **kwargs) -> SubmissionContextData:
        """Alter submission context data to don't show label fields."""
        context_data = super().get_context_data(**kwargs)

        fields = self.form_page.get_form_fields_dict()

        if self.is_export:
            for field_slug in context_data["view"].list_export:
                if field_slug in fields and fields[field_slug].type == "label":
                    context_data["view"].list_export.remove(field_slug)

            return context_data

        header = self.get_header(context_data)
        fields = self.form_page.get_form_fields_dict()

        def show_column(col_idx: int) -> bool:
            field = fields.get(header[col_idx], None)
            return field is None or field.type != "label"

        context_data["data_headings"] = [
            h
            for h in context_data["data_headings"]
            if h["name"] not in fields or fields[h["name"]].type != "label"
        ]

        for row_idx, row in enumerate(context_data["data_rows"]):
            context_data["data_rows"][row_idx]["fields"] = [
                col for col_idx, col in enumerate(row["fields"]) if show_column(col_idx)
            ]

        return context_data
