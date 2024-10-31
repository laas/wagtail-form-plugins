from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from wagtail.contrib.forms.forms import FormBuilder


class FileInputFormBuilder(FormBuilder):
    file_input_max_size = 1 * 1024 * 1024
    file_input_allowed_extensions = ["pdf"]

    def file_input_size_validator(self, value):
        if value.size > self.file_input_max_size:
            size_mo = self.file_input_max_size / (1024 * 1024)
            raise ValidationError(f"File is too big. Max size is {size_mo:.2f} MiB.")

    def create_file_field(self, field_value, options):
        validators = [
            FileExtensionValidator(allowed_extensions=self.file_input_allowed_extensions),
            self.file_input_size_validator,
        ]
        return forms.FileField(**options, validators=validators)
