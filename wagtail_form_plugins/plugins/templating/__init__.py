from django.templatetags.static import static
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import TemplatingFormBlock
from .dicts import DataDict, FormDataDict, ResultDataDict, UserDataDict
from .formatter import TemplatingFormatter
from .forms import TemplatingFormBuilder
from .models import TemplatingFormPage


class Templating(Plugin):
    form_block_class = TemplatingFormBlock
    form_builder_class = TemplatingFormBuilder
    form_page_class = TemplatingFormPage

    @classmethod
    def get_injected_admin_css(cls) -> str:
        return format_html(
            '<link rel="stylesheet" href="{href}">',
            href=static("wagtail_form_plugins/templating/css/form_admin.css"),
        )


__all__ = [
    "DataDict",
    "FormDataDict",
    "ResultDataDict",
    "Templating",
    "TemplatingFormBlock",
    "TemplatingFormPage",
    "TemplatingFormatter",
    "UserDataDict",
]
