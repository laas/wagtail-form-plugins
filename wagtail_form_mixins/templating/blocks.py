# from django.utils.text import format_lazy

from wagtail import blocks
from django.utils.translation import gettext_lazy as _


HELP_TEXT_SUFFIX = '''<span
    class="formbuilder-templating-help_suffix"
    data-message=" {}"
    data-title=" %s"
></span>''' % _("this field supports templating syntax, such as {user.full_name}")


class TemplatingFormBlock(blocks.StreamBlock):
    def get_block_class(self):
        raise NotImplementedError('Missing get_block_class() in the RulesBlockMixin super class.')

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            if 'initial' in child_block.child_blocks:
                child_block.child_blocks['initial'].field.help_text += HELP_TEXT_SUFFIX

        super().__init__(local_blocks, search_index, **kwargs)


# TODO: generalize
class TemplatingEmailFormBlock(blocks.StreamBlock):
    def get_block_class(self):
        raise NotImplementedError('Missing get_block_class() in the RulesBlockMixin super class.')

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            for field_name in ['subject', 'message', 'recipient_list']:
                # child_block.child_blocks[field_name].field.help_text += HELP_TEXT_SUFFIX
                pass

        super().__init__(local_blocks, search_index, **kwargs)
