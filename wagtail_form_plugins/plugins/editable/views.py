"""View classes for the Conditional Fields plugin."""

from django.utils.html import format_html

from wagtail_form_plugins.streamfield.dicts import (
    SubmissionContextData,
    SubmissionContextDataHeading,
)
from wagtail_form_plugins.streamfield.views import StreamFieldSubmissionsListView

from .models import StreamFieldFormPage


class EditableSubmissionsListView(StreamFieldSubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    def get_context_data(self, **kwargs) -> SubmissionContextData:
        """Alter submission context data to format results."""
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        header: SubmissionContextDataHeading = {"name": "edit_btn", "label": "Edit", "order": None}
        context_data["data_headings"].append(header)

        submissions = self.get_submissions(context_data)

        for row_idx, row in enumerate(context_data["data_rows"]):
            submission = submissions[row["model_id"]]

            link_html = format_html(
                '<a class="w-header-button button" href="{url}?edit={submission_id}">edit</a>',
                url=submission.page.url,
                submission_id=row["model_id"],
            )
            context_data["data_rows"][row_idx]["fields"].append(link_html)

        return context_data
