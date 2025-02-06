from wagtail.contrib.forms.views import SubmissionsListView


class ConditionalFieldsSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        for row_idx, row in enumerate(context_data["data_rows"]):
            context_data["data_rows"][row_idx]["fields"] = [
                "-" if val is None else val for val in row["fields"]
            ]

        return context_data
