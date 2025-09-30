from wagtail_form_plugins.streamfield import FormField, StreamFieldFormBuilder


class ConditionalFieldsFormBuilder(StreamFieldFormBuilder):
    def __init__(self, fields: list[FormField]):
        super().__init__(fields)
        self.extra_field_options += ["rule"]
