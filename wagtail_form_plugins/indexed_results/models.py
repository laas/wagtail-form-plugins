"""Models definition for the Indexed Results form plugin."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.forms.models import AbstractFormSubmission

from wagtail_form_plugins.base.models import FormMixin


class IndexedResultsSubmission(AbstractFormSubmission):
    """A mixin used to store the form user in the submission."""

    index = models.IntegerField(default=0)

    def get_data(self):
        """Return dict with form data."""
        return {
            **super().get_data(),
            "index": self.index,
        }

    def save(self, *args, **kwargs):
        """Save the submission"""
        if self.index == 0:
            qs_submissions = self.get_base_class().objects.filter(page=self.page)
            try:
                self.index = max(qs_submissions.values_list("index", flat=True)) + 1
            except ValueError:  # no submission
                self.index = 1

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class IndexedResultsFormMixin(FormMixin):
    """A mixin used to add indexed result functionnality to a form."""

    def get_data_fields(self):
        """Return a list fields data as tuples of slug and label."""
        return [
            ("index", _("Subscription index")),
            *super().get_data_fields(),
        ]

    class Meta:
        abstract = True
