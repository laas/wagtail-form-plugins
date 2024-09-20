from uuid import UUID

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail import blocks
from wagtail.telepath import register as register_adapter


class ChoiceError(ValidationError):
    def __init__(self, choice) -> None:
        super().__init__(
            _("Select a valid choice. %(value)s is not one of the available choices."),
            "invalid_choice",
            {"value": choice}
        )


def field_validator(choice):
    if choice in ['and', 'or']:
        return

    try:
        UUID(str(choice))
    except ValueError as err:
        raise ChoiceError(choice) from err


def operator_validator(choice):
    valid_operators = ['eq', 'neq', 'lt', 'lte', 'ut', 'ute', 'in', 'nin', 'ct', 'nct', 'c', 'nc']

    if choice not in valid_operators:
        raise ChoiceError(choice)


class FreeChoiceField(forms.ChoiceField):
    def validate(self, value):
        for validate in self.validators:
            validate(value)


class FreeChoiceBlock(blocks.ChoiceBlock):
    def get_field(self, **kwargs):
        return FreeChoiceField(**kwargs)


class BooleanExpressionBuilderBlock(blocks.StructBlock):
    field = FreeChoiceBlock(
        [],
        validators=[field_validator],
        form_classname='formbuilder-beb-field',
    )
    operator = FreeChoiceBlock(
        [("eq", "Equals")],
        validators=[operator_validator],
        form_classname='formbuilder-beb-operator',
    )
    value_char = blocks.CharBlock(
        required=False,
        form_classname='formbuilder-beb-val-char',
    )
    value_number = blocks.DecimalBlock(
        required=False,
        form_classname='formbuilder-beb-val-num',
    )
    value_dropdown = FreeChoiceBlock(
        [],
        required=False,
        validators=[],
        form_classname='formbuilder-beb-val-list',
    )
    value_date = blocks.DateBlock(
        required=False,
        form_classname='formbuilder-beb-val-date',
    )

    class Meta:
        label = _('Visibility condition')
        required = False
        collapsed = True
        icon = "view"


class BooleanExpressionBuilderBlockAdapter(blocks.struct_block.StructBlockAdapter):
    js_constructor = 'forms.blocks.BooleanExpressionBuilderBlock'

    @cached_property
    def media(self):
        streamblock_media = super().media
        return forms.Media(
            js=streamblock_media._js + ['conditional_fields/js/form_builder.js'],
            css=streamblock_media._css
        )
register_adapter(BooleanExpressionBuilderBlockAdapter(), BooleanExpressionBuilderBlock)


class BooleanExpressionBuilderBlockLvl3(BooleanExpressionBuilderBlock):
    class Meta:
        form_classname = 'formbuilder-beb formbuilder-beb-lvl3'


class BooleanExpressionBuilderBlockLvl2(BooleanExpressionBuilderBlock):
    rules = blocks.ListBlock(
        BooleanExpressionBuilderBlockLvl3(),
        label=("Conditions"),
        form_classname='formbuilder-beb-rules',
        default=[],
    )

    class Meta:
        form_classname = 'formbuilder-beb formbuilder-beb-lvl2'


class BooleanExpressionBuilderBlockLvl1(BooleanExpressionBuilderBlock):
    rules = blocks.ListBlock(
        BooleanExpressionBuilderBlockLvl2(),
        label=("Conditions"),
        form_classname='formbuilder-beb-rules',
        default=[],
    )

    class Meta:
        form_classname = 'formbuilder-beb formbuilder-beb-lvl1'


class RulesBlockMixin(blocks.StreamBlock):
    def get_block_class(self):
        raise NotImplementedError('Missing get_block_class() in the RulesBlockMixin super class.')

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        local_blocks = local_blocks or []
        rules = blocks.ListBlock(
            BooleanExpressionBuilderBlockLvl1(),
            label="Visibility condition",
            form_classname='formbuilder-field-block-rules',
            default=[],
            max_num=1,
        )

        for child_block_id, child_block in self.get_block_class().declared_blocks.items():
            new_child_block = child_block.__class__(local_blocks=[
                ('rules', rules)
            ])
            local_blocks += [(child_block_id, new_child_block)]

        super().__init__(local_blocks, search_index, **kwargs)
