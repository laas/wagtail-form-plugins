from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import FileInputFormBlock
from .forms import FileInputFormBuilder
from .models import AbstractFileInput, FileInputFormPage
from .views import FileInputSubmissionsListView


class FileInput(Plugin):
    form_block_class = FileInputFormBlock
    form_builder_class = FileInputFormBuilder
    form_page_class = FileInputFormPage
    submission_list_view_class = FileInputSubmissionsListView


__all__ = [
    "AbstractFileInput",
    "FileInput",
    "FileInputFormBlock",
    "FileInputFormBuilder",
    "FileInputFormPage",
    "FileInputSubmissionsListView",
]
