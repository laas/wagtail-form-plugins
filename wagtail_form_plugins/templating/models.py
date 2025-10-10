"""Models definition for the Templating form plugin."""

from django.forms import BaseForm
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield import (
    StreamFieldFormField,
    StreamFieldFormPage,
    StreamFieldFormSubmission,
)

from .formatter import TemplatingFormatter


class TemplatingFormPage(StreamFieldFormPage):
    """Form mixin for the Templating plugin. Used to format initial values and submissions."""

    templating_formatter_class = TemplatingFormatter

    def format_submission(
        self,
        submission: StreamFieldFormSubmission,
        fields: dict[str, StreamFieldFormField],
        formatter: TemplatingFormatter,
    ) -> None:
        """Format the submission passed to the given context data, using the given formatter."""

        new_submission_data: dict[str, str] = {}
        for data_key, data_value in submission.form_data.items():
            field = fields.get(data_key, None)
            if field is None:
                break

            if field.disabled:
                fmt_data = formatter.format(data_value) if data_value else "-"
                if fmt_data != data_value:
                    new_submission_data[data_key] = fmt_data

        if new_submission_data:
            submission.form_data = {
                **submission.form_data,
                **new_submission_data,
            }
            submission.save()

    # def pre_process_form_submission(self, form: BaseForm) -> dict[str, Any]:
    #     """Return a dictionary containing the attributes to pass to the submission constructor."""
    #     submission_data = super().pre_process_form_submission(form)

    #     return {
    #         **submission_data,
    #         "form_data": {
    #             dk: form.data.get(dk, dv) for dk, dv in submission_data["form_data"].items()
    #         },
    #     }

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        formatter = self.templating_formatter_class(response.context_data, False)

        if request.method == "GET":
            form: BaseForm = response.context_data["form"]
            for field in form.fields.values():
                if field.initial:
                    field.initial = formatter.format(field.initial)

        elif "form" not in response.context_data:
            form_submission: StreamFieldFormSubmission = response.context_data["form_submission"]
            form_page: StreamFieldFormPage = response.context_data["page"]
            form_fields = form_page.get_form_fields_dict()
            self.format_submission(form_submission, form_fields, formatter)
        return response

    class Meta:  # type: ignore
        abstract = True
