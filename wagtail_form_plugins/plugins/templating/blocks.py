"""Blocks definition for the Templating plugin."""

from django.core.validators import validate_email
from django.forms import ValidationError
from django.forms.fields import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from wagtail.blocks.field_block import RichTextBlock

from wagtail_form_plugins.streamfield.blocks import FormFieldBlock, StreamFieldFormBlock
from wagtail_form_plugins.utils import LocalBlocks

from .formatter import TemplatingFormatter

TEMPLATING_HELP_INTRO = _("This field supports the following templating syntax:")

HELP_TEXT_SUFFIX = """<span
    class="formbuilder-templating-help_suffix"
    data-message="{}"
    data-title="%s"
></span>"""  # "{}" are the actual characters to display


def build_help_html(help_text: str) -> str:
    """Return the html code used in the field help tooltip."""
    return HELP_TEXT_SUFFIX % f"{TEMPLATING_HELP_INTRO}\n{help_text}"


class TemplatingFormBlock(StreamFieldFormBlock):
    """A mixin used to add templating functionnality to form field wagtail blocks."""

    templating_formatter_class = TemplatingFormatter

    def __init__(self, local_blocks: LocalBlocks = None, search_index: bool = True, **kwargs):  # noqa:FBT001,FBT002
        super().__init__(local_blocks, search_index, **kwargs)

        self.add_help_messages(self.child_blocks.values(), ["initial"])
        self.override_initial_validators()

    def templating_email_validator(self, email: str) -> None:
        """Validate email field: raise a ValidationError if it contains a wrong template syntax."""
        try:
            if not self.templating_formatter_class.contains_template(email):
                validate_email(email)
        except ValueError as err:
            err_message = _("Wrong template syntax. See tooltip for a list of available keywords.")
            raise ValidationError(err_message) from err

    def override_initial_validators(self) -> None:
        """Disable fields validation if it contains templating syntax."""
        for block_type, block in self.child_blocks.items():
            if "initial" in block.child_blocks and block_type == "email":
                block.child_blocks["initial"].field.validators = [self.templating_email_validator]

    @classmethod
    def add_help_messages(cls, blocks: list[FormFieldBlock], field_names: list[str]) -> None:
        """Add a tooltip to wagtail blocks in order that lists all available template variables."""
        help_msg = cls.templating_formatter_class.help()
        for block in blocks:
            for field_name in field_names:
                if (
                    field_name in block.child_blocks
                    and not isinstance(block.child_blocks[field_name], RichTextBlock)
                    and isinstance(block.child_blocks[field_name].field, (CharField, EmailField))
                ):
                    block.child_blocks[field_name].field.help_text += build_help_html(help_msg)
