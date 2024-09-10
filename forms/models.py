from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.contrib.forms.models import FormMixin, EmailFormMixin
from wagtail.contrib.forms.utils import get_field_clean_name

from .forms import StreamFieldFormBuilder


class StreamFieldFormMixin(FormMixin):
    """A mixin that adds form builder functionality to the page."""

    form_builder = StreamFieldFormBuilder

    def get_form_fields(self):
        return self.form_fields

    def get_data_fields(self):
        data_fields = [
            ("submit_time", _("Submission date")),
        ]

        data_fields += [
            (get_field_clean_name(data["value"]["label"]), data["value"]["label"])
            for data in self.get_form_fields().raw_data
        ]

        return data_fields


class AbstractStreamFieldForm(StreamFieldFormMixin, Page):
    """A Form Page. Pages implementing a form should inherit from it."""

    class Meta:
        abstract = True


class AbstractEmailStreamFieldForm(EmailFormMixin, StreamFieldFormMixin, Page):
    """
    A Form Page that sends email. Inherit from it if your form sends an email.
    """

    class Meta:
        abstract = True
