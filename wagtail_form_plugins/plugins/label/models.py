"""Models definition for the Label plugin."""

from typing import Any

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage


class LabelFormPage(StreamFieldFormPage):
    """Form mixin for the Label plugin."""

    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        """Filter out label fields."""
        enabled_fields = super().get_enabled_fields(form_data)
        form_fields = self.get_form_fields_dict()
        return [slug for slug in enabled_fields if form_fields[slug].type != "label"]

    class Meta:
        abstract = True
