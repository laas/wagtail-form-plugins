from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import ConditionalFieldsFormBlock
from .dicts import FormattedRuleDict, RuleBlockDict, RuleBlockValueDict
from .form_field import ConditionalFieldsFormField
from .forms import ConditionalFieldsFormBuilder
from .hooks import hook_conditional_fields_admin_css
from .models import ConditionalFieldsFormPage
from .views import ConditionalFieldsSubmissionsListView


class ConditionalFields(Plugin):
    form_block_class = ConditionalFieldsFormBlock
    form_field_class = ConditionalFieldsFormField
    form_page_class = ConditionalFieldsFormPage
    form_builder_class = ConditionalFieldsFormBuilder
    submission_list_view_class = ConditionalFieldsSubmissionsListView


__all__ = [
    "ConditionalFieldsFormBlock",
    "ConditionalFieldsFormBuilder",
    "ConditionalFieldsFormField",
    "ConditionalFieldsFormPage",
    "ConditionalFieldsSubmissionsListView",
    "FormattedRuleDict",
    "RuleBlockDict",
    "RuleBlockValueDict",
    "hook_conditional_fields_admin_css",
]
