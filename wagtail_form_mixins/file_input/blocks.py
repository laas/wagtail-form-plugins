from django.utils.translation import gettext_lazy as _

from wagtail_form_mixins.streamfield.blocks import FormFieldBlock, RequiredBlock
from wagtail_form_mixins.base.blocks import FormFieldsBlockMixin


class FileInputFormFieldBlock(FormFieldBlock):
    required = RequiredBlock()

    class Meta:
        icon = "doc-full"
        label = _("File")
        form_classname = "formbuilder-field-block formbuilder-field-block-file"


class FileInputFormBlock(FormFieldsBlockMixin):
    file = FileInputFormFieldBlock()
