from django.utils.translation import gettext_lazy as _
from wagtail.contrib.forms.models import AbstractFormSubmission
from django.contrib.auth import get_user_model
from django.db import models


class MyFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def get_data(self):
        return {
            **super().get_data(),
            "user": self.user,
        }


class NamedFormMixin:
    def get_submission_class(self):
        return MyFormSubmission

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
