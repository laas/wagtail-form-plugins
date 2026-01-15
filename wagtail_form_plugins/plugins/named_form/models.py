"""Models definition for the Named Form form plugin."""

from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import BaseForm
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.streamfield.dicts import SubmissionData
from wagtail_form_plugins.streamfield.models import StreamFieldFormPage, StreamFieldFormSubmission


class AuthFormSubmission(StreamFieldFormSubmission):
    """A form submission class used to store the form user in the submission."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_data(self) -> dict[str, Any]:
        """Return dict with form data."""
        data = super().get_data()

        return {
            **data,
            "user": self.user.get_full_name() if self.user else "-",
            "email": self.user.email if self.user else "-",
        }

    class Meta:
        abstract = True


class AuthFormPage(StreamFieldFormPage):
    """Form mixin for the AuthFormPage plugin."""

    unique_response = models.BooleanField(
        verbose_name=_("Unique response"),
        help_text=_("If checked, the user may fill in the form only once."),
        default=False,
    )

    def get_user_submissions_qs(
        self,
        user: AbstractBaseUser | AnonymousUser,
    ) -> models.QuerySet[StreamFieldFormSubmission]:
        """Return the submissions QuerySet corresponding to the current form and the given user."""
        return self.form_submission_class.objects.filter(page=self).filter(user=user)

    def get_data_fields(self) -> list[tuple[str, Any]]:
        """Return a list fields data as tuples of slug and label."""
        data_fields = super().get_data_fields()

        return [
            ("user", _("Form user")),
            ("email", _("User e-mail")),
            *data_fields,
        ]

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Return a dictionary containing the attributes to pass to the submission constructor."""

        class AuthSubmissionData(SubmissionData):
            user: AbstractBaseUser | None

        submission_data: AuthSubmissionData = super().pre_process_form_submission(form)  # ty: ignore invalid-assignment

        class AuthForm(BaseForm):
            user: AbstractBaseUser

        _form: AuthForm = form  # ty: ignore invalid-assignment

        user = _form.user
        submission_data["user"] = None if isinstance(user, AnonymousUser) else user

        return submission_data

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)

        if self.unique_response and self.get_user_submissions_qs(request.user).exists():
            raise PermissionDenied(_("You have already filled in this form."))

        return response

    class Meta:
        abstract = True
