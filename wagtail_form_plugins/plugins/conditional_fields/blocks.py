"""Block-related classes for conditional fields plugin."""

from uuid import UUID

from django.core.exceptions import ValidationError
from django.forms import Media
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.admin.telepath import register as register_adapter
from wagtail.blocks import struct_block

from wagtail_form_plugins.streamfield import blocks as streamfield_blocks
from wagtail_form_plugins.utils import LocalBlocks


class ChoiceError(ValidationError):
    """A validation error used when the selected choice is not available."""

    def __init__(self, choice: str):
        super().__init__(
            _("Select a valid choice. %(value)s is not one of the available choices."),
            "invalid_choice",
            {"value": choice},
        )


def validate_field(value: str) -> None:
    """Validate a field input used in rules, which can be either a and/or, or the field id."""
    if value in ["and", "or"]:
        return

    try:
        UUID(str(value))
    except ValueError as err:
        raise ChoiceError(value) from err


class RuleBlock(blocks.StructBlock):
    """A struct block used to construct a boolean expression."""

    field = blocks.CharBlock(
        validators=[validate_field],
        form_classname="formbuilder-beb-field",
    )
    operator = blocks.ChoiceBlock(
        [
            ("eq", _("is equal to")),
            ("neq", _("is not equal to")),
            ("is", _("is")),
            ("nis", _("is not")),
            ("lt", _("is lower than")),
            ("lte", _("is lower or equal to")),
            ("ut", _("is upper than")),
            ("ute", _("is upper or equal to")),
            ("bt", _("is before than")),
            ("bte", _("is before or equal to")),
            ("at", _("is after than")),
            ("ate", _("is after or equal to")),
            ("ct", _("contains")),
            ("nct", _("does not contain")),
            ("c", _("is checked")),
            ("nc", _("is not checked")),
        ],
        form_classname="formbuilder-beb-operator",
    )
    value_char = blocks.CharBlock(
        required=False,
        form_classname="formbuilder-beb-val-char",
    )
    value_number = blocks.DecimalBlock(
        required=False,
        form_classname="formbuilder-beb-val-num",
    )
    value_dropdown = blocks.CharBlock(
        required=False,
        form_classname="formbuilder-beb-val-list",
    )
    value_date = blocks.DateBlock(
        required=False,
        form_classname="formbuilder-beb-val-date",
    )
    value_time = blocks.TimeBlock(
        required=False,
        form_classname="formbuilder-beb-val-time",
    )
    value_datetime = blocks.DateTimeBlock(
        required=False,
        form_classname="formbuilder-beb-val-datetime",
    )

    class Meta:
        label = _("Visibility condition")
        required = False
        collapsed = True
        icon = "view"


class RuleBlockAdapter(struct_block.StructBlockAdapter):
    """Inject js and css files to a Wagtail admin page for the boolean expression builder."""

    js_constructor = "forms.blocks.BooleanExpressionBuilderBlock"

    @cached_property
    def media(self) -> Media:
        """Return a Media object containing path to css and js files."""
        streamblock_media = super().media
        js_file_path = "wagtail_form_plugins/conditional_fields/js/form_admin.js"

        return Media(
            js=[*streamblock_media._js, js_file_path],  # noqa: SLF001
            css=streamblock_media._css,  # noqa: SLF001
        )


register_adapter(RuleBlockAdapter(), RuleBlock)


class RuleBlockLvl3(RuleBlock):
    """A struct block used to construct a third-level boolean expression."""

    class Meta:
        form_classname = "formbuilder-beb formbuilder-beb-lvl3"


class RuleBlockLvl2(RuleBlock):
    """A struct block used to construct a second-level boolean expression."""

    rules = blocks.ListBlock(
        RuleBlockLvl3(),
        label=("Conditions"),
        form_classname="formbuilder-beb-rules",
        default=[],
    )

    class Meta:
        form_classname = "formbuilder-beb formbuilder-beb-lvl2"


class RuleBlockLvl1(RuleBlock):
    """A struct block used to construct a first-level boolean expression."""

    rules = blocks.ListBlock(
        RuleBlockLvl2(),
        label=("Conditions"),
        form_classname="formbuilder-beb-rules",
        default=[],
    )

    class Meta:
        form_classname = "formbuilder-beb formbuilder-beb-lvl1"


class ConditionalFieldsFormBlock(streamfield_blocks.StreamFieldFormBlock):
    """Add a rule block to each form field."""

    @classmethod
    def get_field_child_blocks(cls, local_blocks: LocalBlocks = None) -> LocalBlocks:
        """Add to the form field a rule block used to define a condition."""
        local_blocks = super().get_field_child_blocks(local_blocks) or []

        rule = blocks.ListBlock(
            RuleBlockLvl1(),
            label=_("Visibility condition"),
            form_classname="formbuilder-field-block-rule",
            default=[],
            max_num=1,
        )
        local_blocks.append(("rule", rule))

        return local_blocks
