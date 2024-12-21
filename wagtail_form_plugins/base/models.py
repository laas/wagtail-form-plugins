from django.db import models

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

    def get_submission_options(self, form):
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def process_form_submission(self, form):
        options = self.get_submission_options(form)
        return self.get_submission_class().objects.create(**options)

    def format_field_value(self, field_type, field_value):
        return field_value

    class Meta:
        abstract = True
