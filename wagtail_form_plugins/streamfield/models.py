"""Models definition for the Streamfield form plugin."""

from typing import Any

from django.forms import BaseForm

from wagtail_form_plugins.base import BaseField, BaseFormPage
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder
from wagtail_form_plugins.utils import create_links


class StreamFieldFormPage(BaseFormPage):
    """Form mixin for the Streamfield plugin."""

    form_builder = StreamFieldFormBuilder
    fields_attr_name = "form_fields"

    @classmethod
    def field_from_streamfield_data(cls, field_data: dict[str, Any]) -> BaseField:
        """Return the form fields based the streamfield value of the form page form_fields field."""
        base_options = ["slug", "label", "help_text", "is_required", "initial"]

        field_value = field_data["value"]
        return BaseField(
            id=field_data["id"],
            clean_name=field_value["slug"],
            field_type=field_data["type"],
            label=field_value["label"],
            help_text=field_value["help_text"],
            required=field_value["is_required"],
            default_value=field_value.get("initial", None),
            options={k: v for k, v in field_value.items() if k not in base_options},
        )

    def get_form(self, *args, **kwargs) -> BaseForm:  # type: ignore
        """Build and return the form instance."""
        form = super().get_form(*args, **kwargs)

        for field in form.fields.values():
            if field.help_text:
                field.help_text = create_links(str(field.help_text)).replace("\n", "")

        return form

    def get_form_fields(self) -> list[BaseField]:
        """Return the form fields based on streamfield data."""
        steamchild = getattr(self, self.fields_attr_name)
        return [self.field_from_streamfield_data(field_data) for field_data in steamchild.raw_data]

    class Meta:  # type: ignore
        abstract = True
