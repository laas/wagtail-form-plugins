from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from wagtail_form_mixins.streamfield.blocks import FormFieldBlock, RequiredBlock


class FileInputFormFieldBlock(FormFieldBlock):
    required = RequiredBlock()

    class Meta:
        icon = "doc-full"
        label = _("File")
        form_classname = "formbuilder-field-block formbuilder-field-block-file"


class FileInputFormBlock(blocks.StreamBlock):
    file = FileInputFormFieldBlock()
