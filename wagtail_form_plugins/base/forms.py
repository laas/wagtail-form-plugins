from wagtail.contrib.forms.forms import FormBuilder


class FormBuilderMixin(FormBuilder):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_extra_field_options(self):
        extra_field_options = []
        for subclass in self.subclasses:
            if hasattr(subclass, "extra_field_options"):
                extra_field_options += subclass.extra_field_options

        return extra_field_options

    def __init__(self, fields):
        super().__init__(fields)
        self.extra_field_options = []

    def add_extra_field_option(self, field_option):
        self.extra_field_options.append(field_option)
