from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from wagtail.blocks.field_block import RichTextBlock

from wagtail_form_mixins.base.blocks import FormFieldsBlockMixin
from .formatter import TemplatingFormatter

TEMPLATING_HELP_INTRO = _("This field supports the following templating syntax:")

HELP_TEXT_SUFFIX = """<span
    class="formbuilder-templating-help_suffix"
    data-message=" {}"
    data-title=" %s"
></span>"""


def build_templating_help(help):
    help_message = TEMPLATING_HELP_INTRO + "\n"

    for var_prefix, item in help.items():
        help_message += "\n"
        for var_suffix, help_text in item.items():
            help_message += f"• {{{ var_prefix }.{ var_suffix }}}: { help_text }\n"

    return help_message


class TemplatingFormBlock(FormFieldsBlockMixin):
    templating_formatter = TemplatingFormatter

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_blocks().values():
            if "initial" in child_block.child_blocks:
                doc = self.templating_formatter.doc()
                help_text = HELP_TEXT_SUFFIX % build_templating_help(doc)
                child_block.child_blocks["initial"].field.help_text += help_text

        super().__init__(local_blocks, search_index, **kwargs)


class TemplatingEmailFormBlock(blocks.StreamBlock):
    templating_formatter = TemplatingFormatter

    def get_block_class(self):
        raise NotImplementedError("Missing get_block_class() in the RulesBlockMixin super class.")

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            for field_name in ["subject", "message", "recipient_list"]:
                if not isinstance(child_block.child_blocks[field_name], RichTextBlock):
                    doc = self.templating_formatter.doc()
                    help_text = HELP_TEXT_SUFFIX % build_templating_help(doc)
                    child_block.child_blocks[field_name].field.help_text += help_text

        super().__init__(local_blocks, search_index, **kwargs)

    class Meta:
        collapsed = True
