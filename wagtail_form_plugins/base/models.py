from django.db import models

from wagtail.admin.mail import send_mail

from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.views import SubmissionsListView


class FormMixin(models.Model):
    subclasses = []
    form_builder: FormBuilder
    submissions_list_view_class: SubmissionsListView

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_mixins(self):
        return [subclass.__name__ for subclass in self.subclasses]

    def get_submission_attributes(self, form):
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def process_form_submission(self, form):
        submission_attributes = self.get_submission_attributes(form)
        return self.get_submission_class().objects.create(**submission_attributes)

    def format_field_value(self, field_type, field_value):
        return field_value

    def send_email(self, email: dict):
        send_mail(**email)

    class Meta:
        abstract = True
