from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.core.exceptions import PermissionDenied

from wagtail.contrib.forms.models import AbstractFormSubmission

from wagtail_form_mixins.base.models import PluginBase


class NamedFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)

    def get_data(self):
        return {
            **super().get_data(),
            "user": self.user,
        }

    class Meta:
        abstract = True


class NamedFormMixin(PluginBase):
    unique_response = models.BooleanField(
        verbose_name=_("Unique response"),
        help_text=_("If checked, the user may fill in the form only once."),
        default=False,
    )

    def get_user_submissions_qs(self, user):
        return self.get_submission_class().objects.filter(page=self).filter(user=user)

    def get_data_fields(self):
        return [
            ("user", _("Form user")),
            *super().get_data_fields(),
        ]

    def get_submission_options(self, form):
        return {
            **super().get_submission_options(form),
            "user": None if isinstance(form.user, AnonymousUser) else form.user,
        }

    def serve(self, request, *args, **kwargs):
        if self.unique_response and self.get_user_submissions_qs(request.user).exists():
            raise PermissionDenied(_("You have already filled in this form."))

        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True
