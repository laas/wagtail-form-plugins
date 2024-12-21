from wagtail.contrib.forms.views import SubmissionsListView


class NamedSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            for data_row in context["data_rows"]:
                user = data_row["fields"][0]
                data_row["fields"][0] = f"{user.first_name} {user.last_name}" if user else "-"

        return context
