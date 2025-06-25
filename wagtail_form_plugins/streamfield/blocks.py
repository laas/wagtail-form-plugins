"""Blocks definition for the Streamfield plugin."""

from typing import Any

from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.utils.functional import cached_property
from django import forms
from django.core.validators import validate_slug

from wagtail import blocks
from wagtail.telepath import register as register_adapter

from wagtail_form_plugins.base.blocks import FormFieldsBlockMixin


class FormFieldBlock(blocks.StructBlock):
    """A generic struct block containing common fields used in other blocks."""

    label = blocks.CharBlock(
        label=_("Label"),
        help_text=_("Short text describing the field."),
        form_classname="formbuilder-field-block-label",
    )
    identifier = blocks.CharBlock(
        label=_("Identifier"),
        required=True,
        help_text=_("The id used to identify this field, for instance in conditional fields."),
        validators=[validate_slug],
    )
    help_text = blocks.CharBlock(
        label=_("Help text"),
        required=False,
        help_text=_("Text displayed below the label to add more information."),
    )
    disabled = blocks.BooleanBlock(
        label=_("Disabled"),
        required=False,
        help_text=_("Check to make the field not editable by the user."),
    )


class FormFieldBlockAdapter(blocks.struct_block.StructBlockAdapter):
    """Inject javascript and css files to a Wagtail admin page for the form field."""

    js_constructor = "forms.blocks.FormFieldBlock"

    @cached_property
    def media(self):
        """Return a Media object containing path to css and js files."""
        streamblock_media = super().media
        js_file_path = "wagtail_form_plugins/streamfield/js/form_admin.js"

        return forms.Media(
            js=streamblock_media._js + [js_file_path],
        )


register_adapter(FormFieldBlockAdapter(), FormFieldBlock)


class RequiredBlock(blocks.BooleanBlock):
    """A boolean block used to add a Required checkbox on the struct blocks that need it."""

    def __init__(self, condition: str = ""):
        super().__init__(
            required=False,
            help_text=format_lazy(
                _("If checked, {condition} to validate the form."),
                condition=condition or _("this field must be filled"),
            ),
            label=_("Required"),
        )


class ChoiceBlock(blocks.StructBlock):
    """A struct block with a label and initial value used as an item for choice-related blocks."""

    label = blocks.CharBlock(
        label=_("Label"),
        form_classname="formbuilder-choice-label",
    )
    initial = blocks.BooleanBlock(
        label=_("Selected"),
        required=False,
    )

    class Meta:
        label = _("Choice")


class ChoicesList(blocks.ListBlock):
    """A generic list block used as a base to define choice-related blocks."""

    def __init__(self, child_block: Any = None, **kwargs):
        super().__init__(child_block or ChoiceBlock(), search_index=True, **kwargs)

    class Meta:
        label = _("Choices")
        form_classname = "formbuilder-choices"


def init_options(field_type: str):
    return {
        "label": _("Default value"),
        "required": False,
        "help_text": format_lazy(
            _("{field_type} used to pre-fill the field."),
            field_type=field_type,
        ),
    }


class SinglelineFormFieldBlock(FormFieldBlock):
    """A struct block used to build a single line form field."""

    required = RequiredBlock()
    initial = blocks.CharBlock(**init_options(_("Single line text")))
    min_length = blocks.IntegerBlock(
        label=_("Min length"),
        help_text=_("Minimum amount of characters allowed in the field."),
        default=0,
    )
    max_length = blocks.IntegerBlock(
        label=_("Max length"),
        help_text=_("Maximum amount of characters allowed in the field."),
        default=255,
    )

    class Meta:
        icon = "pilcrow"
        label = _("Single line text")
        form_classname = "formbuilder-field-block formbuilder-field-block-singleline"


class MultilineFormFieldBlock(FormFieldBlock):
    """A struct block used to build a multi-line form field."""

    required = RequiredBlock()
    initial = blocks.TextBlock(**init_options(_("Multi-line text")))
    min_length = blocks.IntegerBlock(
        label=_("Min length"),
        help_text=_("Minimum amount of characters allowed in the field."),
        default=0,
    )
    max_length = blocks.IntegerBlock(
        label=_("Max length"),
        help_text=_("Maximum amount of characters allowed in the field."),
        default=1024,
    )

    class Meta:
        icon = "pilcrow"
        label = _("Multi-line text")
        form_classname = "formbuilder-field-block formbuilder-field-block-multiline"


class EmailFormFieldBlock(FormFieldBlock):
    """A struct block used to build an email form field."""

    required = RequiredBlock()
    initial = blocks.EmailBlock(**init_options(_("E-mail")))

    class Meta:
        icon = "mail"
        label = _("E-mail")
        form_classname = "formbuilder-field-block formbuilder-field-block-email"


class NumberFormFieldBlock(FormFieldBlock):
    """A struct block used to build a number form field."""

    required = RequiredBlock()
    initial = blocks.DecimalBlock(**init_options(_("Number")))
    min_value = blocks.IntegerBlock(
        label=_("Min value"),
        help_text=_("Minimum number allowed in the field."),
        required=False,
    )
    max_value = blocks.IntegerBlock(
        label=_("Max value"),
        help_text=_("Maximum number allowed in the field."),
        required=False,
    )

    class Meta:
        icon = "decimal"
        label = _("Number")
        form_classname = "formbuilder-field-block formbuilder-field-block-number"


class URLFormFieldBlock(FormFieldBlock):
    """A struct block used to build an url form field."""

    required = RequiredBlock()
    initial = blocks.URLBlock(**init_options(_("URL")))

    class Meta:
        icon = "link-external"
        label = _("URL")
        form_classname = "formbuilder-field-block formbuilder-field-block-url"


class CheckBoxFormFieldBlock(FormFieldBlock):
    """A struct block used to build a checkbox form field."""

    required = RequiredBlock(_("the box must be checked"))
    initial = blocks.BooleanBlock(
        label=_("Checked"),
        required=False,
        help_text=_("If checked, the box will be checked by default."),
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkbox")
        form_classname = "formbuilder-field-block formbuilder-field-block-checkbox"


class CheckBoxesFormFieldBlock(FormFieldBlock):
    """A struct block used to build a multi-checkboxes form field."""

    required = RequiredBlock(_("at least one box must be checked"))
    choices = ChoicesList(
        ChoiceBlock([("initial", blocks.BooleanBlock(label=_("Checked"), required=False))])
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkboxes")
        form_classname = "formbuilder-field-block formbuilder-field-block-checkboxes"


class DropDownFormFieldBlock(FormFieldBlock):
    """A struct block used to build a dropdown form field."""

    required = RequiredBlock(_("an item must be selected"))
    choices = ChoicesList()

    class Meta:
        icon = "list-ul"
        label = _("Drop down")
        form_classname = "formbuilder-field-block formbuilder-field-block-dropdown"


class MultiSelectFormFieldBlock(FormFieldBlock):
    """A struct block used to build a multi-select dropdown form field."""

    required = RequiredBlock(_("at least one item must be selected"))
    choices = ChoicesList()

    class Meta:
        icon = "list-ul"
        label = _("Multiple select")
        form_classname = "formbuilder-field-block formbuilder-field-block-multiselect"


class RadioFormFieldBlock(FormFieldBlock):
    """A struct block used to build a radio-buttons form field."""

    required = RequiredBlock(_("an item must be selected"))
    choices = ChoicesList()

    class Meta:
        icon = "radio-empty"
        label = _("Radio buttons")
        form_classname = "formbuilder-field-block formbuilder-field-block-radio"


class DateFormFieldBlock(FormFieldBlock):
    """A struct block used to build a date form field."""

    required = RequiredBlock()
    initial = blocks.DateBlock(**init_options(_("Date")))

    class Meta:
        icon = "date"
        label = _("Date")
        form_classname = "formbuilder-field-block formbuilder-field-block-date"


class DateTimeFormFieldBlock(FormFieldBlock):
    """A struct block used to build a date-time form field."""

    required = RequiredBlock()
    initial = blocks.DateTimeBlock(**init_options(_("Date and time")))

    class Meta:
        icon = "time"
        label = _("Date and time")
        form_classname = "formbuilder-field-block formbuilder-field-block-datetime"


class HiddenFormFieldBlock(FormFieldBlock):
    """A struct block used to build an hidden form field."""

    required = RequiredBlock()
    initial = blocks.CharBlock(**init_options(_("Hidden text")))

    class Meta:
        icon = "no-view"
        label = _("Hidden text")
        form_classname = "formbuilder-field-block formbuilder-field-block-hidden"


class StreamFieldFormBlock(FormFieldsBlockMixin):
    """A mixin used to use StreamField in a form builder, by selecting some blocks to add fields."""

    singleline = SinglelineFormFieldBlock()
    multiline = MultilineFormFieldBlock()
    email = EmailFormFieldBlock()
    number = NumberFormFieldBlock()
    url = URLFormFieldBlock()
    checkbox = CheckBoxFormFieldBlock()
    checkboxes = CheckBoxesFormFieldBlock()
    dropdown = DropDownFormFieldBlock()
    multiselect = MultiSelectFormFieldBlock()
    radio = RadioFormFieldBlock()
    date = DateFormFieldBlock()
    datetime = DateTimeFormFieldBlock()
    hidden = HiddenFormFieldBlock()

    class Meta:
        form_classname = "formbuilder-fields-block"
        collapsed = True
