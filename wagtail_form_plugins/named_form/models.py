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

from wagtail.contrib.forms.models import FormSubmission

from wagtail_form_plugins.streamfield import StreamFieldFormPage, StreamFieldFormSubmission
from wagtail_form_plugins.streamfield.models import SubmissionData


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
        return {
            **super().get_data(),
            "user": self.user.get_full_name() if self.user else "-",
            "email": self.user.email if self.user else "-",
        }

    class Meta:  # type: ignore
        abstract = True


class AuthFormPage(StreamFieldFormPage):
    """A form page class used to add named form functionnality to a form, allowing to identify the user who
    answered the form, in order to display it on form results and authorise a user to answer a form
    only once."""

    unique_response = models.BooleanField(
        verbose_name=_("Unique response"),
        help_text=_("If checked, the user may fill in the form only once."),
        default=False,
    )

    def get_user_submissions_qs(
        self,
        user: AbstractBaseUser | AnonymousUser,
    ) -> models.QuerySet[FormSubmission]:
        """Return the submissions QuerySet corresponding to the current form and the given user."""
        return self.get_submission_class().objects.filter(page=self).filter(user=user)

    def get_data_fields(self) -> list[tuple[str, Any]]:
        """Return a list fields data as tuples of slug and label."""
        return [
            ("user", _("Form user")),
            ("email", _("User e-mail")),
            *super().get_data_fields(),
        ]

    def pre_process_form_submission(self, form: BaseForm) -> SubmissionData:
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        submission_data = super().pre_process_form_submission(form)

        user = form.user  # type: ignore
        submission_data["user"] = None if isinstance(user, AnonymousUser) else user  # type: ignore

        return submission_data

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        if self.unique_response and self.get_user_submissions_qs(request.user).exists():
            raise PermissionDenied(_("You have already filled in this form."))

        return super().serve(request, *args, **kwargs)

    class Meta:  # type: ignore
        abstract = True
