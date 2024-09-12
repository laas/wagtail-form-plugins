from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings
from django import forms

from wagtail import blocks
from wagtail.telepath import register as register_adapter


MAX_BOOL_EXPR_OPERANDS = 6
MAX_FIELDS_DEFAULT = 50


class ConditionBlock(blocks.StructBlock):
    field_label = blocks.CharBlock(
        required=False,
        form_classname='formbuilder-block-hidden',
    )
    field_id = blocks.CharBlock(
        required=False,
        form_classname='formbuilder-block-hidden',
    )
    operator = blocks.ChoiceBlock(
        label=_("Operator"),
        default='eq',
        choices=[
            ('eq', 'equals'),
            ('neq', 'not equals'),
        ],
    )
    value = blocks.CharBlock(
        label=_("Value"),
    )

    class Meta:
        icon = 'user'
        form_classname = 'formbuilder-condition-block'


class ConditionBlockAdapter(blocks.struct_block.StructBlockAdapter):
    js_constructor = 'forms.blocks.ConditionBlock'

    @cached_property
    def media(self):
        streamblock_media = super().media
        return forms.Media(
            js=streamblock_media._js + ['forms/js/form_builder.js'],
            css=streamblock_media._css
        )
register_adapter(ConditionBlockAdapter(), ConditionBlock)


class BooleanExpressionBlock(blocks.StreamBlock):
    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        def build_block(i):
            return f"cond_{ i + 1 }", ConditionBlock(group=" Fields")

        local_blocks = local_blocks or []
        max_fields = getattr(settings, "WAGTAILFORMS_MAX_FIELDS", MAX_FIELDS_DEFAULT)
        local_blocks += [build_block(i) for i in range(max_fields)]
        super().__init__(local_blocks, search_index, **kwargs)

    class Meta:
        label = _('Visibility condition')
        max_num = 1
        required = False
        group = "Boolean group"
        collapsed = True
        form_classname = 'formbuilder-boolean-expression-block'


class BooleanExpressionBlockAdapter(blocks.stream_block.StreamBlockAdapter):
    js_constructor = 'forms.blocks.BooleanExpressionBlock'

    @cached_property
    def media(self):
        streamblock_media = super().media
        return forms.Media(
            js=streamblock_media._js + ['forms/js/form_builder.js'],
            css=streamblock_media._css
        )
register_adapter(BooleanExpressionBlockAdapter(), BooleanExpressionBlock)


class BooleanExpressionBlockLvl2(BooleanExpressionBlock):
    bool_and = BooleanExpressionBlock(
        label="AND",
        min_num=2,
        max_num=MAX_BOOL_EXPR_OPERANDS,
    )
    bool_or = BooleanExpressionBlock(
        label="OR",
        min_num=2,
        max_num=MAX_BOOL_EXPR_OPERANDS,
    )


class BooleanExpressionBlockLvl1(BooleanExpressionBlock):
    bool_and = BooleanExpressionBlockLvl2(
        label="AND",
        min_num=2,
        max_num=MAX_BOOL_EXPR_OPERANDS,
    )
    bool_or = BooleanExpressionBlockLvl2(
        label="OR",
        min_num=2,
        max_num=MAX_BOOL_EXPR_OPERANDS,
    )


class FormFieldBlock(blocks.StructBlock):
    label = blocks.CharBlock(
        label=_("Label"),
        help_text=_("Short text describing the field.")
    )
    help_text = blocks.CharBlock(
        label=_("Help text"),
        required=False,
        help_text=_("Text displayed below the label to add more information."),
    )
    required = blocks.BooleanBlock(
        label=_("Required"),
        required=False,
        help_text=_("If checked, this field must be filled to validate the form."),
    )
    # name = blocks.CharBlock(required=False, form_classname='formbuilder-block-hidden')

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        local_blocks = local_blocks or []
        local_blocks += [('visibility_condition', BooleanExpressionBlockLvl1())]
        super().__init__(local_blocks, search_index, **kwargs)

    class Meta:
        form_classname = "formbuilder-field-block"


class FormFieldBlockAdapter(blocks.struct_block.StructBlockAdapter):
    js_constructor = 'forms.blocks.FormFieldBlock'

    @cached_property
    def media(self):
        streamblock_media = super().media
        return forms.Media(
            js=streamblock_media._js + ['forms/js/form_builder.js'],
            css=streamblock_media._css
        )
register_adapter(FormFieldBlockAdapter(), FormFieldBlock)


class ChoiceBlock(blocks.StructBlock):
    label = blocks.CharBlock(
        label=_("Label"),
    )
    initial = blocks.BooleanBlock(
        label=_("Selected"),
        required=False,
    )

    class Meta:
        label = _("Choice")


class SinglelineFormFieldBlock(FormFieldBlock):
    initial = blocks.CharBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Text used to pre-fill the field."),
    )
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


class MultilineFormFieldBlock(FormFieldBlock):
    initial = blocks.TextBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Multi-line text used to pre-fill the text area."),
    )
    min_length = blocks.IntegerBlock(
        label=_("Min length"),
        help_text=_("Minimum amount of characters allowed in the text area."),
        default=0,
    )
    max_length = blocks.IntegerBlock(
        label=_("Max length"),
        help_text=_("Maximum amount of characters allowed in the text area."),
        default=1024,
    )

    class Meta:
        icon = "pilcrow"
        label = _("Multi-line text")


class EmailFormFieldBlock(FormFieldBlock):
    initial = blocks.EmailBlock(
        label=_("Default value"),
        required=False,
        help_text=_("E-mail used to pre-fill the field."),
    )

    class Meta:
        icon = "mail"
        label = _("E-mail")


class NumberFormFieldBlock(FormFieldBlock):
    initial = blocks.DecimalBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Number used to pre-fill the field."),
    )
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


class URLFormFieldBlock(FormFieldBlock):
    initial = blocks.URLBlock(
        label=_("Default value"),
        required=False,
        help_text=_("URL used to pre-fill the field."),
    )

    class Meta:
        icon = "link-external"
        label = _("URL")


class CheckBoxFormFieldBlock(FormFieldBlock):
    initial = blocks.BooleanBlock(
        label=_("Checked"),
        required=False,
        help_text=_("If checked, the checkbox will be checked by default."),
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkbox")


class CheckBoxesFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock([("initial", blocks.BooleanBlock(label=_("Checked"), required=False))]),
        label=_("Choices"),
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkboxes")


class DropDownFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Drop down")


class MultiSelectFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Multiple select")


class RadioFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "radio-empty"
        label = _("Radio buttons")


class DateFormFieldBlock(FormFieldBlock):
    initial = blocks.DateBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Date used to pre-fill the field."),
    )

    class Meta:
        icon = "date"
        label = _("Date")


class DateTimeFormFieldBlock(FormFieldBlock):
    initial = blocks.DateTimeBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Date and time used to pre-fill the field."),
    )

    class Meta:
        icon = "time"
        label = _("Date and time")


class HiddenFormFieldBlock(FormFieldBlock):
    initial = blocks.CharBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Text used to pre-fill the field."),
    )

    class Meta:
        icon = "no-view"
        label = _("Hidden field")


class FormFieldsBlock(blocks.StreamBlock):
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


def validate_emails(value):
    email_variables = ['{author_email}', '{user_email}']

    for address in value.split(","):
        if address.strip() not in email_variables:
            validate_email(address.strip())


class Email:
    def __init__(self, recipient_list: str, subject: str, message: str, ):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

    def format(self):
        return {
            "type": "email_to_send",
            "value": {
                "recipient_list": self.recipient_list,
                "subject": self.subject,
                "message": self.message.replace('\n','</p><p>'),
            }
        }


class EmailsToSendBlock(blocks.StreamBlock):
    email_to_send = blocks.StructBlock([
        ('recipient_list', blocks.CharBlock(
            label=_("Recipient list"),
            validators=[validate_emails],
            help_text=_("E-mail addresses of the recipients, separated by comma."),
        )),
        ('subject', blocks.CharBlock(
            label=_("Subject"),
            help_text=_("The subject of the e-mail."),
        )),
        ('message', blocks.RichTextBlock(
            label=_("Message"),
            help_text=_("The body of the e-mail."),
        )),
    ])
