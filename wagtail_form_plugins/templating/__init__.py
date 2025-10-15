from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import TemplatingFormBlock
from .dicts import DataDict, FormDataDict, ResultDataDict, UserDataDict
from .formatter import TemplatingFormatter
from .forms import TemmplatingFormBuilder
from .hooks import hook_templating_admin_css
from .models import TemplatingFormPage


class Templating(Plugin):
    form_block_class = TemplatingFormBlock
    form_builder_class = TemmplatingFormBuilder
    form_page_class = TemplatingFormPage


__all__ = [
    "DataDict",
    "FormDataDict",
    "ResultDataDict",
    "Templating",
    "TemplatingFormBlock",
    "TemplatingFormPage",
    "TemplatingFormatter",
    "UserDataDict",
    "hook_templating_admin_css",
]
