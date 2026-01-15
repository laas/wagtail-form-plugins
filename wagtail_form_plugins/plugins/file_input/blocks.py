"""Blocks definition for the File Input plugin."""

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from wagtail_form_plugins.streamfield.blocks import FormFieldBlock, StreamFieldFormBlock


class FileInputFormFieldBlock(FormFieldBlock):
    """A wagtail struct block used to add a file field when building a form."""

    allowed_extensions = blocks.MultipleChoiceBlock(
        label=_("Allowed file extensions"),
        choices=[(ext, ext) for ext in settings.FORMS_FILE_UPLOAD_AVAILABLE_EXTENSIONS],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        icon = "doc-full"
        label = _("File")
        form_classname = "formbuilder-field-block formbuilder-field-block-file"


class FileInputFormBlock(StreamFieldFormBlock):
    """Form fields block used to add file input functionnality to form field wagtail blocks."""

    # settings.FORMS_FILE_UPLOAD_AVAILABLE_EXTENSIONS
    file = FileInputFormFieldBlock()
