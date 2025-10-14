"""Form-related classes for the File Input plugin."""

from typing import Any, ClassVar

from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.forms import FileField, ValidationError, widgets
from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.streamfield.form_field import StreamFieldFormField
from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder


class FileInputFormBuilder(StreamFieldFormBuilder):
    """Form builder class that adds file input functionnality to a form."""

    file_input_max_size = 1 * 1024 * 1024
    file_input_allowed_extensions: ClassVar = ["pdf"]

    def __init__(self, fields: list[StreamFieldFormField]):
        super().__init__(fields)
        self.extra_field_options += ["allowed_extensions"]

    def file_input_size_validator(self, value: File) -> None:
        """Validate the size of a file."""
        if value.size > self.file_input_max_size:
            size_mo = self.file_input_max_size / (1024 * 1024)
            error_msg = f"File is too big. Max size is {size_mo:.2f} MiB."
            raise ValidationError(error_msg)

    def create_file_field(self, form_field: Any, options: dict[str, Any]) -> FileField:
        """Create a Django file field."""
        allowed_ext = form_field.options["allowed_extensions"]
        validators = [
            FileExtensionValidator(allowed_extensions=allowed_ext),
            self.file_input_size_validator,
        ]
        str_allowed = ",".join([f".{ext}" for ext in allowed_ext])
        options["help_text"] += f" {_('Allowed:')} {str_allowed}"
        widget = widgets.FileInput(attrs={"slug": form_field.slug, "accept": str_allowed})
        return FileField(widget=widget, **options, validators=validators)
