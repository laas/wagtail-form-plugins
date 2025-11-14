from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder, StreamFieldFormField


class ConditionalFieldsFormBuilder(StreamFieldFormBuilder):
    def __init__(self, fields: list[StreamFieldFormField]):
        super().__init__(fields)
        self.extra_field_options += ["rule"]
