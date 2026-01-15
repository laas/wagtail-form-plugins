"""Blocks definition for the Streamfield plugin."""

from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from wagtail_form_plugins.streamfield.blocks import StreamFieldFormBlock


class LabelFormFieldBlock(blocks.StructBlock):
    """A struct block used to build a label form field."""

    label = blocks.CharBlock(label=_("Title"), form_classname="formbuilder-field-block-label")
    help_text = blocks.CharBlock(label=_("Sub-title"), required=False)

    class Meta:
        icon = "title"
        label = _("Label")
        form_classname = "formbuilder-field-block formbuilder-field-block-label"


class LabelFormBlock(StreamFieldFormBlock):
    """A form field block used to add label functionnality to form field wagtail blocks."""

    label = LabelFormFieldBlock()
