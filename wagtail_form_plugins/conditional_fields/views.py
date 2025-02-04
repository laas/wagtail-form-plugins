from wagtail.contrib.forms.views import SubmissionsListView


class ConditionalFieldsSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for idx, row in enumerate(context["data_rows"]):
            context["data_rows"][idx]["fields"] = [
                "-" if val is None else val for val in row["fields"]
            ]

        return context
