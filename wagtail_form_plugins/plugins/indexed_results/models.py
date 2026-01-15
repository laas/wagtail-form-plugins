"""Models definition for the Indexed Results form plugin."""

from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage, StreamFieldFormSubmission


class IndexedResultsFormSubmission(StreamFieldFormSubmission):
    """A form submission used to store the form user in the submission."""

    index = models.IntegerField(default=0)

    def get_data(self) -> dict[str, Any]:
        """Return dict with form data."""
        data = super().get_data()

        return {
            **data,
            "index": self.index,
        }

    def save(self, *args, **kwargs) -> None:
        """Insert the index value before to save the form submission."""
        if self.index == 0:
            qs_submissions = self.__class__.objects.filter(page=self.page)
            try:
                self.index = max(qs_submissions.values_list("index", flat=True)) + 1
            except ValueError:  # no submission
                self.index = 1

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class IndexedResultsFormPage(StreamFieldFormPage):
    """A form page used to add indexed result functionnality to a form."""

    def get_data_fields(self) -> list[tuple[str, Any]]:
        """Return a list fields data as tuples of slug and label."""
        data_fields = super().get_data_fields()

        return [
            ("index", _("Subscription index")),
            *data_fields,
        ]

    class Meta:
        abstract = True
