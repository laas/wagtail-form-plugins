from wagtail_form_plugins.base.models import FormMixin
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder, Field


class StreamFieldFormMixin(FormMixin):
    form_builder = StreamFieldFormBuilder

    def get_form_fields(self):
        return [Field.from_streamfield_data(field_data) for field_data in self.form_fields.raw_data]

    class Meta:
        abstract = True
