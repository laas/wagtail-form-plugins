# from django.utils.text import format_lazy

from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from wagtail.blocks.field_block import RichTextBlock

TEMPLATING_HELP_INTRO = _("This field supports the following templating syntax:")

HELP_TEXT_SUFFIX = """<span
    class="formbuilder-templating-help_suffix"
    data-message=" {}"
    data-title=" %s"
></span>"""

DEFAULT_TEMPLATING_DOC = {
    "user": {
        "login": _("the form user login (ex: “alovelace”)"),
        "first_name": _("the form user first name (ex: “Ada”)"),
        "last_name": _("the form user last name (ex: “Lovelace”)"),
        "full_name": _("the form user first name and last name (ex: “Ada Lovelace”)"),
    },
    "author": {
        "login": _("the form author login (ex: “shawking”)"),
        "first_name": _("the form author first name (ex: “Stephen”)"),
        "last_name": _("the form user last name (ex: “Hawking”)"),
        "full_name": _("the form user first name and last name (ex: “Stephen Hawking”)"),
    },
    "form": {
        "title": _("the form title (ex: “My form”)"),
        "url": _("the form url (ex: “https://example.com/form/my-form”)"),
        "publish_date": _("the date on which the form was published (ex: “15/10/2024”)"),
        "publish_time": _("the time on which the form was published (ex: “13h37”)"),
    },
    "result": {
        "data": _("the form data as a list (ex: “- my_first_question: 42”)"),
        "publish_date": _("the date on which the form was completed (ex: “16/10/2024”)"),
        "publish_time": _("the time on which the form was completed (ex: “12h06”)"),
    },
    "field_label": {
        "my_first_question": _("the label of the related question (ex: “My first question”)"),
    },
    "field_value": {
        "my_first_question": _("the value of the related question (ex: “42”)"),
    },
}


def build_templating_help(help):
    help_message = TEMPLATING_HELP_INTRO + "\n"

    for var_prefix, item in help.items():
        help_message += "\n"
        for var_suffix, help_text in item.items():
            help_message += f"• {{{ var_prefix }.{ var_suffix }}}: { help_text }\n"

    return help_message


class TemplatingFormBlock(blocks.StreamBlock):
    templating_doc = DEFAULT_TEMPLATING_DOC

    def get_block_class(self):
        raise NotImplementedError("Missing get_block_class() in the RulesBlockMixin super class.")

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            if "initial" in child_block.child_blocks:
                help_text = HELP_TEXT_SUFFIX % build_templating_help(self.templating_doc)
                child_block.child_blocks["initial"].field.help_text += help_text

        super().__init__(local_blocks, search_index, **kwargs)


class TemplatingEmailFormBlock(blocks.StreamBlock):
    templating_doc = DEFAULT_TEMPLATING_DOC

    def get_block_class(self):
        raise NotImplementedError("Missing get_block_class() in the RulesBlockMixin super class.")

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        for child_block in self.get_block_class().declared_blocks.values():
            for field_name in ["subject", "message", "recipient_list"]:
                if not isinstance(child_block.child_blocks[field_name], RichTextBlock):
                    help_text = HELP_TEXT_SUFFIX % build_templating_help(self.templating_doc)
                    child_block.child_blocks[field_name].field.help_text += help_text

        super().__init__(local_blocks, search_index, **kwargs)

    class Meta:
        collapsed = True
