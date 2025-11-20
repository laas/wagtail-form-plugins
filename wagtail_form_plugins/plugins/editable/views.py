"""View classes for the Conditional Fields plugin."""

from typing import TYPE_CHECKING, Any

from django.utils.html import format_html

from wagtail.contrib.forms.views import SubmissionsListView

from .models import StreamFieldFormPage

if TYPE_CHECKING:
    from wagtail.contrib.forms.models import FormSubmission


class StreamFieldSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as displaying `-` when a value is set to None."""

    form_page: StreamFieldFormPage

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Alter submission context data to format results."""
        ctx_data = super().get_context_data(**kwargs)

        submissions: dict[str, FormSubmission] = {sub.id: sub for sub in ctx_data["submissions"]}
        ctx_data["data_headings"].append({"name": "edit_button", "label": "Edit", "order": None})

        for row_idx, row in enumerate(ctx_data["data_rows"]):
            submission = submissions[row["model_id"]]

            link_html = format_html(
                '<a class="w-header-button button" href="{url}?edit={submission_id}">edit</a>',
                url=submission.page.url,
                submission_id=row["model_id"],
            )
            ctx_data["data_rows"][row_idx]["fields"].append(link_html)

        return ctx_data
