"""Form-related classes for the Streamfield plugin."""

from typing import Any

from django.forms import widgets

from wagtail_form_plugins.base import BaseFormBuilder
from wagtail_form_plugins.streamfield.forms import CharField


class Label(widgets.TextInput):
    """A widget used to only display a label without a form input."""

    def __init__(self, attrs: dict | None = None):
        super().__init__({**(attrs or {}), "style": "display: none"})


class LabelFormBuilder(BaseFormBuilder):
    """Form builder class that use streamfields to define form fields in form admin page."""

    def create_label_field(self, field: Any, options: dict[str, Any]) -> CharField:
        """Create a label without html input field."""

        return CharField(widget=Label(), **options)
