"""Base classes for form builder mixins."""

from wagtail.contrib.forms.forms import FormBuilder


class FormBuilderMixin(FormBuilder):
    """Base class for form builder mixins."""

    subclasses = []

    def __init__(self, fields):
        super().__init__(fields)
        self.extra_field_options = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_extra_field_options(self):
        """Get all the extra field options from all subclasses."""
        extra_field_options = []
        for subclass in self.subclasses:
            if hasattr(subclass, "extra_field_options"):
                extra_field_options += subclass.extra_field_options

        return extra_field_options

    def add_extra_field_option(self, field_option):
        """Add an extra field option to the form builder."""
        self.extra_field_options.append(field_option)
