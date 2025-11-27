"""Form-related classes for the Streamfield plugin."""

from typing import Any

from django.forms import CharField, widgets

from wagtail_form_plugins.streamfield.form_field import StreamFieldFormField
from wagtail_form_plugins.streamfield.models import StreamFieldFormBuilder


class LabelFormBuilder(StreamFieldFormBuilder):
    """Form builder class that use streamfields to define form fields in form admin page."""

    def create_label_field(
        self,
        _field: StreamFieldFormField,
        options: dict[str, Any],
    ) -> CharField:
        """Create a label without html input field."""
        widget_attrs = {
            **options.pop("widget_attrs"),
            "style": "display: none",
            "class": "form-title-input",
        }
        return CharField(widget=widgets.TextInput(attrs=widget_attrs), **options)
