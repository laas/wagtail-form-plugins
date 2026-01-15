"""Blocks definition for the Streamfield plugin."""

from typing import Any, ClassVar

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import Media
from django.utils.functional import cached_property
from django.utils.text import format_lazy
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.admin.telepath import register as register_adapter
from wagtail.blocks import Block, FieldBlock, StreamValue, struct_block

from wagtail_form_plugins.utils import LocalBlocks, validate_slug


class SlugBlock(blocks.CharBlock):
    """A CharBlock that displays duplication errors."""

    def __init__(self, *arg, **kwargs):
        kwargs["validators"] = [validate_slug]
        super().__init__(*arg, **kwargs)

    def clean(self, value: str) -> FieldBlock:
        """Raise a ValidationError if the block class has a duplicates attribute."""
        cleaned = super().clean(value)

        if duplicates := getattr(self, "duplicates", {}).get(value, None):
            msg = _("The id '{field_id}' is already in use in fields {duplicates}.").format(
                field_id=value,
                duplicates=", ".join([f"n°{idx + 1}" for idx in duplicates]),
            )
            raise ValidationError(msg)

        return cleaned


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


class FormFieldBlock(blocks.StructBlock):
    """A generic struct block containing common fields used in other blocks."""

    label = blocks.CharBlock(
        label=_("Label"),
        help_text=_("Short text describing the field."),
        form_classname="formbuilder-field-block-label",
    )
    slug = SlugBlock(
        label=_("Slug"),
        required=True,
        help_text=_("Identifier used to identify this field, for instance in conditional fields."),
    )
    help_text = blocks.CharBlock(
        label=_("Help text"),
        required=False,
        help_text=_("Text displayed below the label to add more information."),
    )
    is_required = RequiredBlock()
    disabled = blocks.BooleanBlock(
        label=_("Disabled"),
        required=False,
        help_text=_("Check to make the field not editable by the user."),
    )


class FormFieldBlockAdapter(struct_block.StructBlockAdapter):
    """Inject javascript and css files to a Wagtail admin page for the form field."""

    js_constructor = "forms.blocks.FormFieldBlock"

    @cached_property
    def media(self) -> Media:
        """Return a Media object containing path to css and js files."""
        streamblock_media = super().media
        js_file_path = "wagtail_form_plugins/streamfield/js/form_admin.js"

        return Media(js=[*streamblock_media._js, js_file_path])  # noqa: SLF001


register_adapter(FormFieldBlockAdapter(), FormFieldBlock)


def init_options(field_type: str) -> dict[str, Any]:
    """Return default options for initial field of all blocks."""
    return {
        "label": _("Default value"),
        "required": False,
        "help_text": format_lazy(
            _("{field_type} used to pre-fill the field."),
            field_type=field_type,
        ),
    }


class ChoiceBlock(blocks.StructBlock):
    """To Be Deleted."""


class ChoicesList(blocks.ListBlock):
    """To Be Deleted."""

    def __init__(self, child_block: Block | None = None, **kwargs):
        super().__init__(child_block or ChoiceBlock(), **kwargs)


class SinglelineFormFieldBlock(FormFieldBlock):
    """A struct block used to build a single line form field."""

    initial = blocks.CharBlock(**init_options(__("Single line text")))
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

    initial = blocks.TextBlock(**init_options(__("Multi-line text")))
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

    initial = blocks.CharBlock(**init_options(__("E-mail")), validators=[validate_email])

    class Meta:
        icon = "mail"
        label = _("E-mail")
        form_classname = "formbuilder-field-block formbuilder-field-block-email"


class NumberFormFieldBlock(FormFieldBlock):
    """A struct block used to build a number form field."""

    initial = blocks.DecimalBlock(**init_options(__("Number")))
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

    initial = blocks.URLBlock(**init_options(__("URL")))

    class Meta:
        icon = "link-external"
        label = _("URL")
        form_classname = "formbuilder-field-block formbuilder-field-block-url"


class CheckBoxFormFieldBlock(FormFieldBlock):
    """A struct block used to build a checkbox form field."""

    is_required = RequiredBlock(__("the box must be checked"))
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

    is_required = RequiredBlock(__("at least one box must be checked"))
    choices = blocks.TextBlock(label=_("Choices list, one per line"))

    class Meta:
        icon = "tick-inverse"
        label = _("Checkboxes")
        form_classname = "formbuilder-field-block formbuilder-field-block-checkboxes"


class DropDownFormFieldBlock(FormFieldBlock):
    """A struct block used to build a dropdown form field."""

    is_required = RequiredBlock(__("an item must be selected"))
    choices = blocks.TextBlock(label=_("Choices list, one per line"))

    class Meta:
        icon = "list-ul"
        label = _("Drop down")
        form_classname = "formbuilder-field-block formbuilder-field-block-dropdown"


class MultiSelectFormFieldBlock(FormFieldBlock):
    """A struct block used to build a multi-select dropdown form field."""

    is_required = RequiredBlock(__("at least one item must be selected"))
    choices = blocks.TextBlock(label=_("Choices list, one per line"))

    class Meta:
        icon = "list-ul"
        label = _("Multiple select")
        form_classname = "formbuilder-field-block formbuilder-field-block-multiselect"


class RadioFormFieldBlock(FormFieldBlock):
    """A struct block used to build a radio-buttons form field."""

    is_required = RequiredBlock(__("an item must be selected"))
    choices = blocks.TextBlock(label=_("Choices list, one per line"))

    class Meta:
        icon = "radio-empty"
        label = _("Radio buttons")
        form_classname = "formbuilder-field-block formbuilder-field-block-radio"


class DateFormFieldBlock(FormFieldBlock):
    """A struct block used to build a date form field."""

    initial = blocks.DateBlock(**init_options(__("Date")))

    class Meta:
        icon = "date"
        label = _("Date")
        form_classname = "formbuilder-field-block formbuilder-field-block-date"


class TimeFormFieldBlock(FormFieldBlock):
    """A struct block used to build a time form field."""

    initial = blocks.TimeBlock(**init_options(__("Time")))

    class Meta:
        icon = "time"
        label = _("Time")
        form_classname = "formbuilder-field-block formbuilder-field-block-time"


class DateTimeFormFieldBlock(FormFieldBlock):
    """A struct block used to build a date-time form field."""

    initial = blocks.DateTimeBlock(**init_options(__("Date and time")))

    class Meta:
        icon = "date"
        label = _("Date and time")
        form_classname = "formbuilder-field-block formbuilder-field-block-datetime"


class HiddenFormFieldBlock(FormFieldBlock):
    """A struct block used to build an hidden form field."""

    initial = blocks.CharBlock(**init_options(__("Hidden text")))

    class Meta:
        icon = "no-view"
        label = _("Hidden text")
        form_classname = "formbuilder-field-block formbuilder-field-block-hidden"


class BaseFormBlock(blocks.StreamBlock):
    """A base StreamBlock that exposes the get_blocks function."""

    subclasses: ClassVar = []

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        """Add the subclass in the subclasses attribute."""
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @classmethod
    def get_blocks(cls) -> dict[str, Block]:
        """Get all the declared blocks from all subclasses."""
        declared_blocks = {}

        for subclass in cls.subclasses:
            declared_blocks.update(subclass.declared_blocks)

        return declared_blocks

    @classmethod
    def get_field_child_blocks(cls, local_blocks: LocalBlocks = None) -> LocalBlocks:
        """Return the form fields child blocks. Can be extended to add more blocks to each field."""
        return local_blocks or []

    def __init__(self, local_blocks: LocalBlocks = None, search_index: bool = True, **kwargs):  # noqa:FBT001,FBT002
        local_blocks = local_blocks or []

        if field_child_blocks := self.get_field_child_blocks():
            for child_block_id, child_block in self.get_blocks().items():
                new_child_block = child_block.__class__(local_blocks=field_child_blocks)
                local_blocks += [(child_block_id, new_child_block)]

        super().__init__(local_blocks, search_index, **kwargs)


class StreamFieldFormBlock(BaseFormBlock):
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
    time = TimeFormFieldBlock()
    datetime = DateTimeFormFieldBlock()
    hidden = HiddenFormFieldBlock()

    class Meta:
        form_classname = "formbuilder-fields-block"
        collapsed = True

    @classmethod
    def get_duplicates(cls, blocks: StreamValue) -> dict[str, str]:
        """Return a dict containing slug duplicates in the given blocks."""
        duplicates = {}
        for idx, slug in enumerate([block.value.get("slug", None) for block in blocks]):
            if slug:
                duplicates[slug] = [*duplicates.get(slug, []), idx]
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    def clean(self, value: StreamValue, ignore_required_constraints: bool = False) -> StreamValue:  # noqa: FBT001, FBT002
        """Add duplicates attribute in the block class."""
        cleaned = super().clean(value, ignore_required_constraints)

        if len(value) > 0:
            block = value[0].block.child_blocks.get("slug", None)
            if block:
                block.duplicates = self.get_duplicates(value)

        return cleaned
