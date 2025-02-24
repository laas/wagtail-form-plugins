"""Models definition for the Named Form form plugin."""

from django.forms import Form
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser, User
from django.db import models
from django.core.exceptions import PermissionDenied
from django.conf import settings

from wagtail.contrib.forms.models import AbstractFormSubmission

from wagtail_form_plugins.base.models import FormMixin


class NamedFormSubmission(AbstractFormSubmission):
    """A mixin used to store the form user in the submission."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_data(self):
        """Return dict with form data."""
        return {
            **super().get_data(),
            "user": self.user.get_full_name() if self.user else "-",
            "email": self.user.email if self.user else "-",
        }

    class Meta:
        abstract = True


class NamedFormMixin(FormMixin):
    """A mixin used to add named form functionnality to a form, allowing to identify the user who
    answered the form, in order to display it on form results and authorise a user to answer a form
    only once."""

    unique_response = models.BooleanField(
        verbose_name=_("Unique response"),
        help_text=_("If checked, the user may fill in the form only once."),
        default=False,
    )

    def get_user_submissions_qs(self, user: User):
        """Return the submissions QuerySet corresponding to the current form and the given user."""
        return self.get_submission_class().objects.filter(page=self).filter(user=user)

    def get_data_fields(self):
        """Return a list fields data as tuples of slug and label."""
        return [
            ("user", _("Form user")),
            ("email", _("User e-mail")),
            *super().get_data_fields(),
        ]

    def get_submission_attributes(self, form: Form):
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        return {
            **super().get_submission_attributes(form),
            "user": None if isinstance(form.user, AnonymousUser) else form.user,
        }

    def serve(self, request: HttpRequest, *args, **kwargs):
        """Serve the form page."""
        if self.unique_response and self.get_user_submissions_qs(request.user).exists():
            raise PermissionDenied(_("You have already filled in this form."))

        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True
