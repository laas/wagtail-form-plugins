"""Blocks definition for the Streamfield plugin."""

from django.utils.translation import gettext_lazy as _

from wagtail_form_plugins.streamfield import StreamFieldFormBlock
from wagtail_form_plugins.streamfield.blocks import FormFieldBlock, RequiredBlock


class LabelFormFieldBlock(FormFieldBlock):
    """A struct block used to build a label form field."""

    is_required = RequiredBlock()

    class Meta:  # type: ignore
        icon = "title"
        label = _("Label")
        form_classname = "formbuilder-field-block formbuilder-field-block-label"


class LabelFormBlock(StreamFieldFormBlock):
    """A form field block used to add label functionnality to form field wagtail blocks."""

    label = LabelFormFieldBlock()
