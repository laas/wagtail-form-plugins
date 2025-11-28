"""Conditional fields: make a field appear or not depending on the value of a previous field."""

from django.templatetags.static import static
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import ConditionalFieldsFormBlock
from .dicts import FormattedRuleDict, RuleBlockDict, RuleBlockValueDict
from .form_field import ConditionalFieldsFormField
from .models import ConditionalFieldsFormPage


class ConditionalFields(Plugin):
    form_block_class = ConditionalFieldsFormBlock
    form_field_class = ConditionalFieldsFormField
    form_page_class = ConditionalFieldsFormPage

    @classmethod
    def get_injected_admin_css(cls) -> str:
        return format_html(
            '<link rel="stylesheet" href="{href}">',
            href=static("wagtail_form_plugins/conditional_fields/css/form_admin.css"),
        )


__all__ = [
    "ConditionalFieldsFormBlock",
    "ConditionalFieldsFormField",
    "ConditionalFieldsFormPage",
    "FormattedRuleDict",
    "RuleBlockDict",
    "RuleBlockValueDict",
]
