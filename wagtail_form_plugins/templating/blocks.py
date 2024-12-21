from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from wagtail.blocks.field_block import RichTextBlock

from wagtail_form_plugins.base.blocks import FormFieldsBlockMixin
from .formatter import TemplatingFormatter

TEMPLATING_HELP_INTRO = _("This field supports the following templating syntax:")

HELP_TEXT_SUFFIX = """<span
    class="formbuilder-templating-help_suffix"
    data-message="{}"
    data-title="%s"
></span>"""  # "{}" are the actual characters to display


def build_help_html(help_text):
    return HELP_TEXT_SUFFIX % f"{ TEMPLATING_HELP_INTRO }\n{ help_text }"


class TemplatingFormBlock(FormFieldsBlockMixin):
    formatter_class = TemplatingFormatter

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_blocks().values():
            if "initial" in child_block.child_blocks:
                help_html = build_help_html(self.formatter_class.help())
                child_block.child_blocks["initial"].field.help_text += help_html

        super().__init__(local_blocks, search_index, **kwargs)


class TemplatingEmailFormBlock(blocks.StreamBlock):
    formatter_class = TemplatingFormatter

    def get_block_class(self):
        raise NotImplementedError("Missing get_block_class() in the RulesBlockMixin super class.")

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            for field_name in ["subject", "message", "recipient_list", "reply_to"]:
                if not isinstance(child_block.child_blocks[field_name], RichTextBlock):
                    help_text = build_help_html(self.formatter_class.help())
                    child_block.child_blocks[field_name].field.help_text += help_text

        super().__init__(local_blocks, search_index, **kwargs)

    class Meta:
        collapsed = True
