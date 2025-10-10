"""Blocks definition for the Templating plugin."""

from typing import Any

from django.forms.fields import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from wagtail.blocks.field_block import RichTextBlock

from wagtail_form_plugins.streamfield.blocks import StreamFieldFormBlock
from wagtail_form_plugins.utils import LocalBlocks

from .formatter import TemplatingFormatter

TEMPLATING_HELP_INTRO = _("This field supports the following templating syntax:")

HELP_TEXT_SUFFIX = """<span
    class="formbuilder-templating-help_suffix"
    data-message="{}"
    data-title="%s"
></span>"""  # "{}" are the actual characters to display


def build_help_html(help_text: str) -> str:
    return HELP_TEXT_SUFFIX % f"{TEMPLATING_HELP_INTRO}\n{help_text}"


class TemplatingFormBlock(StreamFieldFormBlock):
    """A mixin used to add templating functionnality to form field wagtail blocks."""

    templating_formatter_class = TemplatingFormatter

    def __init__(self, local_blocks: LocalBlocks = None, search_index: bool = True, **kwargs):
        blocks = list(self.get_blocks().values())
        self.add_help_messages(blocks, ["initial"], self.templating_formatter_class.help())
        super().__init__(local_blocks, search_index, **kwargs)

    @classmethod
    def add_help_messages(cls, blocks: list[Any], field_names: list[str], help_msg: str) -> None:
        """Add a tooltip to wagtail blocks in order that lists all available template variables."""
        for block in blocks:
            for n in field_names:
                if (
                    n in block.child_blocks
                    and not isinstance(block.child_blocks[n], RichTextBlock)
                    and isinstance(block.child_blocks[n].field, (CharField, EmailField))
                ):
                    block.child_blocks[n].field.help_text += build_help_html(help_msg)
