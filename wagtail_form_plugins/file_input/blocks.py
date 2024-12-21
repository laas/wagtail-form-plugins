from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from wagtail import blocks

from wagtail_form_plugins.streamfield.blocks import FormFieldBlock, RequiredBlock
from wagtail_form_plugins.base.blocks import FormFieldsBlockMixin


class FileInputFormFieldBlock(FormFieldBlock):
    required = RequiredBlock()
    allowed_extensions = blocks.MultipleChoiceBlock(
        label=_("Allowed file extensions"),
        choices=[(ext, ext) for ext in settings.FORMS_FILE_UPLOAD_AVAILABLE_EXTENSIONS],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        icon = "doc-full"
        label = _("File")
        form_classname = "formbuilder-field-block formbuilder-field-block-file"


class FileInputFormBlock(FormFieldsBlockMixin):
    file = FileInputFormFieldBlock()
