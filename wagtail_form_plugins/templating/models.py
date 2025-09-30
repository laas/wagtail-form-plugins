"""Models definition for the Templating form plugin."""

from typing import Any

from django.forms import Form
from django.http import HttpRequest, HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse

from wagtail_form_plugins.streamfield import StreamFieldFormPage
from wagtail_form_plugins.templating.formatter import TemplatingFormatter
from wagtail_form_plugins.utils import create_links


class TemplatingFormPage(StreamFieldFormPage):
    """Form mixin for the Templating plugin. Used to format initial values and submissions."""

    templating_formatter_class = TemplatingFormatter

    def format_submission(
        self,
        context_data: dict,
        formatter: TemplatingFormatter,
        post: QueryDict,
    ) -> None:
        """Format the submission passed to the given context data, using the given formatter."""
        form_submission = context_data["form_submission"]

        disabled_fields = [
            field.value["slug"]
            for field in context_data["page"].form_fields
            if field.value.get("disabled")
        ]

        fields_with_choices = [
            field.value["slug"]
            for field in context_data["page"].form_fields
            if field.value.get("choices")
        ]

        new_submission_data = {}
        for data_key, data_value in form_submission.form_data.items():
            if data_key in fields_with_choices:
                new_submission_data[data_key] = ",".join(post.getlist(data_key))

            if data_key in disabled_fields:
                fmt_data = formatter.format(data_value) if data_value else "-"
                if fmt_data != data_value:
                    new_submission_data[data_key] = fmt_data

        if new_submission_data:
            form_submission.form_data = {
                **form_submission.form_data,
                **new_submission_data,
            }
            form_submission.save()

    def get_submission_attributes(self, form: Form) -> dict[str, Any]:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        attributes = super().get_submission_attributes(form)

        return {
            **attributes,
            "form_data": {dk: form.data.get(dk, dv) for dk, dv in attributes["form_data"].items()},
        }

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        formatter = self.templating_formatter_class(response.context_data)

        if request.method == "GET":
            for field in response.context_data["form"].fields.values():
                if field.initial:
                    field.initial = formatter.format(field.initial)

        elif "form" not in response.context_data:
            self.format_submission(response.context_data, formatter, request.POST)
            formatter = self.templating_formatter_class(response.context_data)

            for email in response.context_data["page"].emails_to_send:
                for field_name in ["subject", "message", "recipient_list", "reply_to"]:
                    fmt_value = formatter.format(str(email.value[field_name]))
                    if field_name == "message":
                        fmt_value = create_links(fmt_value.replace("\n", "<br/>\n"))
                    email.value[field_name] = fmt_value
        return response

    class Meta:  # type: ignore
        abstract = True
