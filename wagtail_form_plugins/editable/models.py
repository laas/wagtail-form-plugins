"""Models definition for the Editable form plugin."""

from django.forms.widgets import HiddenInput, TextInput, FileInput
from django.forms.fields import CharField
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from wagtail.contrib.forms.utils import get_field_clean_name

from wagtail_form_plugins.base.models import FormMixin


class EditableFormMixin(FormMixin):
    """Form mixin for the Editable plugin, allowing to edit a form result via the `edit` field."""

    def serve(self, request, *args, **kwargs):
        """Serve the form page."""
        admins = get_user_model().objects.filter(groups__name=self.get_group_name())

        if request.user in admins:
            if request.method == "POST" and "edit" in request.POST:
                submission_id = int(request.POST["edit"])
                submission = get_object_or_404(self.get_submission_class(), pk=submission_id)
                form = self.get_form(request.POST, request.FILES, page=self, user=request.user)
                file_fields = [
                    get_field_clean_name(field.label)
                    for field in form.fields.values()
                    if isinstance(field.widget, FileInput)
                ]

                if form.is_valid():
                    attrs = self.get_submission_attributes(form)
                    attrs["form_data"] = {
                        k: v if k not in file_fields or v else submission.form_data[k]
                        for k, v in attrs["form_data"].items()
                    }
                    for attr_key, attr_value in attrs.items():
                        setattr(submission, attr_key, attr_value)
                    submission.save()
                    redirect_args = {"page_id": self.pk}
                    return redirect(reverse("wagtailforms:list_submissions", kwargs=redirect_args))

            elif request.method == "GET" and "edit" in request.GET:
                submission_id = int(request.GET["edit"])
                submission = get_object_or_404(self.get_submission_class(), pk=submission_id)
                form = self.get_form(submission.form_data, page=self)

                for field in form.fields.values():
                    if isinstance(field.widget, HiddenInput):
                        field.widget = TextInput()

                edit_attrs = {"value": request.GET["edit"]}
                form.fields["edit"] = CharField(widget=HiddenInput(attrs=edit_attrs))

                context = self.get_context(request)
                context["form"] = form
                return TemplateResponse(request, self.get_template(request), context)

        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True
