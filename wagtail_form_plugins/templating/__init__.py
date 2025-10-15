from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import TemplatingFormBlock
from .formatter import TemplatingFormatter
from .forms import TemmplatingFormBuilder
from .hooks import hook_templating_admin_css
from .models import TemplatingFormPage


class Templating(Plugin):
    form_block_class = TemplatingFormBlock
    form_builder_class = TemmplatingFormBuilder
    form_page_class = TemplatingFormPage


__all__ = [
    "Templating",
    "TemplatingFormBlock",
    "TemplatingFormPage",
    "TemplatingFormatter",
    "hook_templating_admin_css",
]
