from django.utils.translation import gettext_lazy as _

from wagtail import blocks


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


class RequiredBlock(blocks.BooleanBlock):
    def __init__(self, help_text=None, **kwargs):
        super().__init__(
            False,
            help_text or _("If checked, this field must be filled to validate the form."),
            **kwargs,
        )

    label = _("Required")
    form_classname='formbuilder-field-block-required'


class ChoiceBlock(blocks.StructBlock):
    label = blocks.CharBlock(
        label=_("Label"),
        form_classname='formbuilder-choice-label',
    )
    initial = blocks.BooleanBlock(
        label=_("Selected"),
        required=False,
    )

    class Meta:
        label = _("Choice")


class SinglelineFormFieldBlock(FormFieldBlock):
    required = RequiredBlock()
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
    required = RequiredBlock()
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
    required = RequiredBlock()
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
    required = RequiredBlock()
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
    required = RequiredBlock()
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
    required = RequiredBlock(_("If checked, the box must be checked to validate the form."))
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
    required = RequiredBlock(_("If checked, at least one box must be checked to validate the form."))
    choices = blocks.ListBlock(
        ChoiceBlock([("initial", blocks.BooleanBlock(label=_("Checked"), required=False))]),
        label=_("Choices"),
        form_classname='formbuilder-choices',
    )

    class Meta:
        icon = "tick-inverse"
        label = _("Checkboxes")
        form_classname = "formbuilder-field-block formbuilder-checkboxes-field-block"


class DropDownFormFieldBlock(FormFieldBlock):
    required = RequiredBlock(_("If checked, an item must be selected to validate the form."))
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
        form_classname='formbuilder-choices',
    )

    class Meta:
        icon = "list-ul"
        label = _("Drop down")
        form_classname = "formbuilder-field-block formbuilder-dropdown-field-block"


class MultiSelectFormFieldBlock(FormFieldBlock):
    required = RequiredBlock(_("If checked, at least one item must be selected to validate the form."))
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
        form_classname='formbuilder-choices',
    )

    class Meta:
        icon = "list-ul"
        label = _("Multiple select")
        form_classname = "formbuilder-field-block formbuilder-multiselect-field-block"


class RadioFormFieldBlock(FormFieldBlock):
    required = RequiredBlock(_("If checked, a button must be selected to validate the form."))
    choices = blocks.ListBlock(
        ChoiceBlock(),
        label=_("Choices"),
        form_classname='formbuilder-choices',
    )

    class Meta:
        icon = "radio-empty"
        label = _("Radio buttons")
        form_classname = "formbuilder-field-block formbuilder-radio-field-block"


class DateFormFieldBlock(FormFieldBlock):
    required = RequiredBlock()
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
    required = RequiredBlock()
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
    required = RequiredBlock()
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
