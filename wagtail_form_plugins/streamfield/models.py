"""Models definition for the Streamfield form plugin."""

from wagtail_form_plugins.base.models import FormPageMixin
from wagtail_form_plugins.streamfield.forms import BaseField, StreamFieldFormBuilder
from wagtail_form_plugins.utils import create_links


class StreamFieldFormPageMixin(FormPageMixin):
    """Form mixin for the Streamfield plugin."""

    form_builder = StreamFieldFormBuilder

    def get_form(self, *args, **kwargs):
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        for field in form.fields.values():
            if field.help_text:
                field.help_text = create_links(field.help_text).replace("\n", "")

        return form

    def get_form_fields(self):
        """Return the form fields based on streamfield data."""
        return [BaseField.from_streamfield_data(f_data) for f_data in self.form_fields.raw_data]

    class Meta:
        abstract = True
