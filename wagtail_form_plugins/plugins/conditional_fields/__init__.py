from django.templatetags.static import static
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import ConditionalFieldsFormBlock
from .dicts import FormattedRuleDict, RuleBlockDict, RuleBlockValueDict
from .form_field import ConditionalFieldsFormField
from .forms import ConditionalFieldsFormBuilder
from .models import ConditionalFieldsFormPage
from .views import ConditionalFieldsSubmissionsListView


class ConditionalFields(Plugin):
    form_block_class = ConditionalFieldsFormBlock
    form_field_class = ConditionalFieldsFormField
    form_page_class = ConditionalFieldsFormPage
    form_builder_class = ConditionalFieldsFormBuilder
    submission_list_view_class = ConditionalFieldsSubmissionsListView
    injected_admin_css = format_html(
        '<link rel="stylesheet" href="{href}">',
        href=static("wagtail_form_plugins/conditional_fields/css/form_admin.css"),
    )


__all__ = [
    "ConditionalFieldsFormBlock",
    "ConditionalFieldsFormBuilder",
    "ConditionalFieldsFormField",
    "ConditionalFieldsFormPage",
    "ConditionalFieldsSubmissionsListView",
    "FormattedRuleDict",
    "RuleBlockDict",
    "RuleBlockValueDict",
]
