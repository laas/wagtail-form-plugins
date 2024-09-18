from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django import forms

from wagtail import blocks
from wagtail.telepath import register as register_adapter


class BooleanExpressionBuilderBlock(blocks.StructBlock):
    field = blocks.ChoiceBlock(
        [],
        form_classname='formbuilder-beb-field'
    )
    operator = blocks.ChoiceBlock(
        [],
        form_classname='formbuilder-beb-operator'
    )
    value_char = blocks.CharBlock(
        form_classname='formbuilder-beb-val-char'
    )
    value_number = blocks.DecimalBlock(
        form_classname='formbuilder-beb-val-num'
    )
    value_dropdown = blocks.ChoiceBlock(
        [],
        form_classname='formbuilder-beb-val-list'
    )
    value_date = blocks.DateBlock(
        form_classname='formbuilder-beb-val-date'
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
            js=streamblock_media._js + ['forms/js/form_builder.js'],
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
        min_num=2,
        default=[],
    )

    class Meta:
        form_classname = 'formbuilder-beb formbuilder-beb-lvl2'


class BooleanExpressionBuilderBlockLvl1(BooleanExpressionBuilderBlock):
    rules = blocks.ListBlock(
        BooleanExpressionBuilderBlockLvl2(),
        label=("Conditions"),
        form_classname='formbuilder-beb-rules',
        min_num=2,
        default=[],
    )

    class Meta:
        form_classname = 'formbuilder-beb formbuilder-beb-lvl1'


class FormFieldBlock(blocks.StructBlock):
    label = blocks.CharBlock(
        label=_("Label"),
        help_text=_("Short text describing the field."),
        form_classname='formbuilder-field-block-label',
    )
    help_text = blocks.CharBlock(
        label=_("Help text"),
        required=False,
        help_text=_("Text displayed below the label to add more information."),
        form_classname='formbuilder-field-block-help',
    )
    required = blocks.BooleanBlock(
        label=_("Required"),
        required=False,
        help_text=_("If checked, this field must be filled to validate the form."),
        form_classname='formbuilder-field-block-required',
    )

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        rules = blocks.ListBlock(
            BooleanExpressionBuilderBlockLvl1(),
            label=_("Visibility condition"),
            form_classname="formbuilder-field-block-rules",
            default=[],
            max_num=1,
        )
        local_blocks = (local_blocks or []) + [('rules', rules)]
        super().__init__(local_blocks, search_index, **kwargs)


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
        form_classname = "formbuilder-field-block formbuilder-singleline-field-block"


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
        form_classname = "formbuilder-field-block formbuilder-multiline-field-block"


class EmailFormFieldBlock(FormFieldBlock):
    initial = blocks.EmailBlock(
        label=_("Default value"),
        required=False,
        help_text=_("E-mail used to pre-fill the field."),
    )

    class Meta:
        icon = "mail"
        label = _("E-mail")
        form_classname = "formbuilder-field-block formbuilder-email-field-block"


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
        form_classname = "formbuilder-field-block formbuilder-number-field-block"


class URLFormFieldBlock(FormFieldBlock):
    initial = blocks.URLBlock(
        label=_("Default value"),
        required=False,
        help_text=_("URL used to pre-fill the field."),
    )

    class Meta:
        icon = "link-external"
        label = _("URL")
        form_classname = "formbuilder-field-block formbuilder-url-field-block"


class CheckBoxFormFieldBlock(FormFieldBlock):
    initial = blocks.BooleanBlock(
        label=_("Checked"),
        required=False,
        help_text=_("If checked, the checkbox will be checked by default."),
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkbox")
        form_classname = "formbuilder-field-block formbuilder-checkbox-field-block"


class CheckBoxesFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock([("initial", blocks.BooleanBlock(label=_("Checked"), required=False))]),
        label=_("Choices"),
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkboxes")
        form_classname = "formbuilder-field-block formbuilder-checkboxes-field-block"


class DropDownFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Drop down")
        form_classname = "formbuilder-field-block formbuilder-dropdown-field-block"


class MultiSelectFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "list-ul"
        label = _("Multiple select")
        form_classname = "formbuilder-field-block formbuilder-multiselect-field-block"


class RadioFormFieldBlock(FormFieldBlock):
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
    )

    class Meta:
        icon = "radio-empty"
        label = _("Radio buttons")
        form_classname = "formbuilder-field-block formbuilder-radio-field-block"


class DateFormFieldBlock(FormFieldBlock):
    initial = blocks.DateBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Date used to pre-fill the field."),
    )

    class Meta:
        icon = "date"
        label = _("Date")
        form_classname = "formbuilder-field-block formbuilder-date-field-block"


class DateTimeFormFieldBlock(FormFieldBlock):
    initial = blocks.DateTimeBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Date and time used to pre-fill the field."),
    )

    class Meta:
        icon = "time"
        label = _("Date and time")
        form_classname = "formbuilder-field-block formbuilder-datetime-field-block"


class HiddenFormFieldBlock(FormFieldBlock):
    initial = blocks.CharBlock(
        label=_("Default value"),
        required=False,
        help_text=_("Text used to pre-fill the field."),
    )

    class Meta:
        icon = "no-view"
        label = _("Hidden field")
        form_classname = "formbuilder-field-block formbuilder-hidden-field-block"


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

    class Meta:
        form_classname = "formbuilder-fields-block"


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


class EmailsToSendStructBlock(blocks.StructBlock):
    recipient_list = blocks.CharBlock(
        label=_("Recipient list"),
        validators=[validate_emails],
        help_text=_("E-mail addresses of the recipients, separated by comma."),
    )

    subject = blocks.CharBlock(
        label=_("Subject"),
        help_text=_("The subject of the e-mail."),
    )

    message = blocks.RichTextBlock(
        label=_("Message"),
        help_text=_("The body of the e-mail."),
    )


class EmailsToSendBlock(blocks.StreamBlock):
    email_to_send = EmailsToSendStructBlock()
