"""Blocks definition for the Streamfield plugin."""

from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.base.blocks import FormFieldsBlockMixin
from wagtail_form_plugins.streamfield.blocks import RequiredBlock, FormFieldBlock


class LabelFormFieldBlock(FormFieldBlock):
    """A struct block used to build a label form field."""

    required = RequiredBlock()

    class Meta:
        icon = "title"
        label = _("Label")
        form_classname = "formbuilder-field-block formbuilder-field-block-label"


class LabelFormBlock(FormFieldsBlockMixin):
    """A mixin used to add label functionnality to form field wagtail blocks."""

    label = LabelFormFieldBlock()
