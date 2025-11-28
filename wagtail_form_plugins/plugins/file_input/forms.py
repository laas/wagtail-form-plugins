"""Form-related classes for the File Input plugin."""

from typing import Any

from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.forms import FileField, ValidationError, widgets
from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder

from .form_field import FileInputFormField


class FileInputFormBuilder(StreamFieldFormBuilder):
    """Form builder class that adds file input functionnality to a form."""

    file_input_max_size = 1 * 1024 * 1024

    def file_input_size_validator(self, value: File) -> None:
        """Validate the size of a file."""
        if value.size > self.file_input_max_size:
            size_mo = self.file_input_max_size / (1024 * 1024)
            error_msg = f"File is too big. Max size is {size_mo:.2f} MiB."
            raise ValidationError(error_msg)

    def create_file_field(
        self,
        form_field: FileInputFormField,
        options: dict[str, Any],
    ) -> FileField:
        """Create a Django file field."""
        validators = [
            FileExtensionValidator(allowed_extensions=form_field.allowed_extensions),
            self.file_input_size_validator,
        ]
        str_allowed = ",".join([f".{ext}" for ext in form_field.allowed_extensions])
        options["help_text"] += f" {_('Allowed:')} {str_allowed}"
        w_attrs = {
            **options.pop("widget_attrs"),
            "accept": str_allowed,
        }

        return FileField(widget=widgets.FileInput(attrs=w_attrs), **options, validators=validators)
