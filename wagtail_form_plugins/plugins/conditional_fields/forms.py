"""Form-related classes for the Conditional Fields plugin."""

from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder, StreamFieldFormField


class ConditionalFieldsFormBuilder(StreamFieldFormBuilder):
    """Form builder class that adds Conditional fields functionnality to a form."""

    def __init__(self, fields: list[StreamFieldFormField]):
        super().__init__(fields)
        self.extra_field_options += ["rule"]
