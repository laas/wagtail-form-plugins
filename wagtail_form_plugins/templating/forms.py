from typing import Any

from django import forms
from django.core.validators import validate_email

from wagtail_form_plugins.streamfield.form_field import StreamFieldFormField
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder


class TemmplatingFormBuilder(StreamFieldFormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""

    @staticmethod
    def _email_validator(email: str) -> None:
        if "{" in email and "}" in email:
            return
        validate_email(email)

    def create_email_field(  # type: ignore
        self, form_field: StreamFieldFormField, options: dict[str, Any]
    ) -> forms.EmailField:
        options["validators"] = [self._email_validator]
        return super().create_email_field(form_field, options)
