from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import TemplatingFormBlock
from .formatter import ResultDataDict, TemplatingFormatter, UserDataDict
from .hooks import hook_templating_admin_css
from .models import TemplatingFormPage


class Templating(Plugin):
    form_block_class = TemplatingFormBlock
    form_page_class = TemplatingFormPage


__all__ = [
    "ResultDataDict",
    "Templating",
    "TemplatingFormBlock",
    "TemplatingFormPage",
    "TemplatingFormatter",
    "UserDataDict",
    "hook_templating_admin_css",
]
