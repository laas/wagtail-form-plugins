from typing import Any

from wagtail_form_plugins.streamfield import StreamFieldFormPage


class LabelFormPage(StreamFieldFormPage):
    def get_enabled_fields(self, form_data: dict[str, Any]) -> list[str]:
        enabled_fields = super().get_enabled_fields(form_data)
        form_fields = self.get_form_fields_dict()
        return [slug for slug in enabled_fields if form_fields[slug].type != "label"]

    class Meta:  # type: ignore
        abstract = True
