"""Models definition for the Editable form plugin."""

from typing import Any

from django.forms.fields import CharField
from django.forms.widgets import FileInput, HiddenInput, TextInput
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from wagtail_form_plugins.streamfield import StreamFieldFormPage


class EditableFormPage(StreamFieldFormPage):
    """Form page for the Editable plugin, allowing to edit a form result via the `edit` field."""

    def edit_post(self, request: HttpRequest) -> str:
        """Handle POST request of form page edition, return redirect url or empty string."""
        submission_id = int(request.POST["edit"])
        submission = get_object_or_404(self.get_submission_class(), pk=submission_id)
        form = self.get_form(request.POST, request.FILES, page=self, user=submission.user)  # type: ignore
        form_fields = list(form.fields.values())

        for field in form_fields:
            if isinstance(field.widget, FileInput):
                field.required = False
        form.full_clean()

        if form.is_valid():
            file_fields = [f.clean_name for f in form_fields if isinstance(f.widget, FileInput)]  # type: ignore

            attrs = self.get_submission_attributes(form)  # type: ignore
            attrs["form_data"] = {
                k: v if k not in file_fields or v else submission.form_data[k]
                for k, v in attrs["form_data"].items()
            }
            for attr_key, attr_value in attrs.items():
                setattr(submission, attr_key, attr_value)
            submission.save()
            redirect_args = {"page_id": self.pk}
            return reverse("wagtailforms:list_submissions", kwargs=redirect_args)

        return ""

    def edit_get(self, request: HttpRequest) -> dict[str, Any]:
        """Handle GET request of form page edition, return context."""
        submission_id = int(request.GET["edit"])
        submission = get_object_or_404(self.get_submission_class(), pk=submission_id)
        form = self.get_form(submission.form_data, page=self)

        for field in form.fields.values():
            field.disabled = False
            if isinstance(field.widget, HiddenInput):
                field.widget = TextInput()

            if isinstance(field.widget, FileInput):
                field.required = False

        edit_attrs = {"value": request.GET["edit"]}
        form.fields["edit"] = CharField(widget=HiddenInput(attrs=edit_attrs))

        return {**self.get_context(request), "form": form}

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""

        if self.permissions_for_user(request.user).can_edit():
            if request.method == "POST" and "edit" in request.POST:
                redirect_url = self.edit_post(request)
                if redirect_url:
                    return redirect(redirect_url)  # type: ignore

            elif request.method == "GET" and "edit" in request.GET:
                context = self.edit_get(request)
                return TemplateResponse(request, self.get_template(request), context)

        return super().serve(request, *args, **kwargs)

    class Meta:  # type: ignore
        abstract = True
