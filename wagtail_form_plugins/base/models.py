"""Base classes for form mixins."""

from typing import Any
from django.db import models
from django.forms import Form

from wagtail.admin.mail import send_mail

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.views import SubmissionsListView


class FormMixin(models.Model):
    """Base model class for builder mixins."""

    subclasses = []
    form_builder: FormBuilder
    submissions_list_view_class: SubmissionsListView

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_mixins(self):
        """Return all form builder mixins."""
        return [subclass.__name__ for subclass in self.subclasses]

    def get_submission_attributes(self, form: Form):
        """Return a dictionary containing the attributes to pass to the submission constructor."""
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def process_form_submission(self, form: Form):
        """Create and return submission instance."""
        submission_attributes = self.get_submission_attributes(form)
        return self.get_submission_class().objects.create(**submission_attributes)

    def format_field_value(self, field_type: str, field_value: Any):
        """Format the field value. Used to display user-friendly values in result table."""
        return field_value

    def send_mail(self, email: dict):
        """Send an e-mail. Override this to change the behavior (ie. print the email instead)."""
        send_mail(**email)

    class Meta:
        abstract = True
