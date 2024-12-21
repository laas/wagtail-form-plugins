from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import AbstractFormSubmission
from wagtail_form_plugins.base.models import FormMixin


class IndexedResultsSubmission(AbstractFormSubmission):
    index = models.IntegerField(default=0)

    def get_data(self):
        return {
            **super().get_data(),
            "index": self.index,
        }

    def save(self, *args, **kwargs):
        qs_submissions = self.get_model_class().objects.filter(page=self.page)
        try:
            self.index = max(qs_submissions.values_list("index", flat=True)) + 1
        except ValueError:  # no submission
            self.index = 1
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class IndexedResultsFormMixin(FormMixin):
    def get_data_fields(self):
        return [
            ("index", _("Subscription index")),
            *super().get_data_fields(),
        ]

    class Meta:
        abstract = True
