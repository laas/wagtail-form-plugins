from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import PermissionDenied

from wagtail.contrib.forms.models import AbstractFormSubmission


class AbstractNamedFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def get_data(self):
        return {
            **super().get_data(),
            "user": self.user,
        }

    class Meta:
        abstract = True


class NamedFormMixin(models.Model):
    unique_response = models.BooleanField(
        verbose_name=_("Unique response"),
        help_text=_("If checked, the user may fill in the form only once."),
    )

    def get_user_submissions_qs(self, user):
        return self.get_submission_class().objects.filter(page=self).filter(user=user)

    def get_data_fields(self):
        return [
            ("user", _("Form user")),
            *super().get_data_fields(),
        ]

    def process_form_submission(self, form):
        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self,
            user=form.user,
        )

    def serve(self, request, *args, **kwargs):
        if self.unique_response and self.get_user_submissions_qs(request.user).exists():
            raise PermissionDenied(_("You have already filled in this form."))

        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True
