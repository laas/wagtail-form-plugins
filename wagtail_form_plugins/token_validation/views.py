from django.apps import apps
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.db.models.query import QuerySet
from wagtail.contrib.forms.views import SubmissionsListView


class TokenValidationView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        CustomFormSubmission = apps.get_model(app_label=settings.FORMS_SUBMISSION_MODEL)

        submission = get_object_or_404(CustomFormSubmission, pk=kwargs["submission_id"])

        if kwargs["token"] == submission.token:
            submission.validated = True
            submission.save()

        context = {
            "is_validated": submission.validated,
        }

        return render(request, "wagtail_form_plugins/form_validation.html", context)


class TokenValidationSubmissionListView(SubmissionsListView):
    def get_base_queryset(self) -> QuerySet:
        qs: QuerySet = super().get_base_queryset()
        return qs.filter(validated=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails = {sub.id: sub.email for sub in context["submissions"]}

        if not self.is_export:
            for data_row in context["data_rows"]:
                data_row["fields"][0] = f"{emails[data_row['model_id']]}"

        return context
