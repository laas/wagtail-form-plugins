"""Form-related classes for the File Input plugin."""

from typing import Any
from django import forms
from django.core.files.base import File
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError

from wagtail_form_plugins.base.forms import FormBuilderMixin
from wagtail_form_plugins.streamfield.forms import FieldWithIdMixin


class FileField(FieldWithIdMixin, forms.FileField):
    """A Django FileField class with an addititional identifier attribute."""

    pass


class FileInputFormBuilder(FormBuilderMixin):
    """Form builder mixin that adds file input functionnality to a form."""

    file_input_max_size = 1 * 1024 * 1024
    file_input_allowed_extensions = ["pdf"]
    extra_field_options = ["allowed_extensions"]

    def file_input_size_validator(self, value: File):
        """Validate the size of a file."""
        if value.size > self.file_input_max_size:
            size_mo = self.file_input_max_size / (1024 * 1024)
            raise ValidationError(f"File is too big. Max size is {size_mo:.2f} MiB.")

    def create_file_field(self, field_value: Any, options: dict[str, Any]):
        """Create a Django file field."""
        allowed_ext = field_value.options["allowed_extensions"]
        validators = [
            FileExtensionValidator(allowed_extensions=allowed_ext),
            self.file_input_size_validator,
        ]
        str_allowed = ",".join([f".{ ext }" for ext in allowed_ext])
        options["help_text"] += f" { _('Allowed:') } { str_allowed }"
        widget = forms.widgets.FileInput(attrs={"accept": str_allowed})

        return FileField(widget=widget, **options, validators=validators)
