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
        self.add_help_messages(self.get_blocks().values(), ["initial"], self.formatter_class.help())
        super().__init__(local_blocks, search_index, **kwargs)

    @classmethod
    def add_help_messages(cls, blocks, field_names, help_message: str):
        for block in blocks:
            for n in field_names:
                if n in block.child_blocks and not isinstance(block.child_blocks[n], RichTextBlock):
                    block.child_blocks[n].field.help_text += build_help_html(help_message)
