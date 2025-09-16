"""Form-related classes for the Streamfield plugin."""

from typing import Any

from django import forms

from wagtail_form_plugins.base.forms import FormBuilderMixin
from wagtail_form_plugins.streamfield.forms import CharField


class Label(forms.widgets.TextInput):
    """A widget used to only display a label without a form input."""

    def __init__(self, attrs: dict | None = None):
        super().__init__({**(attrs or {}), "style": "display: none"})


class LabelFormBuilder(FormBuilderMixin):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    def create_label_field(self, field: Any, options: dict[str, Any]):
        """Create a label without html input field."""

        return CharField(widget=Label(), **options)
