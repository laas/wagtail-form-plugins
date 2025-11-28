"""File input plugin: allow users to send a file via the form."""

from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import FileInputFormBlock
from .form_field import FileInputFormField
from .forms import FileInputFormBuilder
from .models import AbstractFileInput, DefaultFileInput, FileInputFormPage
from .views import FileInputSubmissionsListView


class FileInput(Plugin):
    """File input plugin: allow users to send a file via the form."""

    form_block_class = FileInputFormBlock
    form_builder_class = FileInputFormBuilder
    form_field_class = FileInputFormField
    form_page_class = FileInputFormPage
    submission_list_view_class = FileInputSubmissionsListView


__all__ = [
    "AbstractFileInput",
    "DefaultFileInput",
    "FileInput",
    "FileInputFormBlock",
    "FileInputFormBuilder",
    "FileInputFormField",
    "FileInputFormPage",
    "FileInputSubmissionsListView",
]
