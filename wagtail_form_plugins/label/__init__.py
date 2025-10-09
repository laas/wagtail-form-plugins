from wagtail_form_plugins.streamfield.plugin import Plugin

from .blocks import LabelFormBlock
from .forms import LabelFormBuilder
from .models import LabelFormPage
from .views import LabelSubmissionsListView


class Label(Plugin):
    form_block_class = LabelFormBlock
    form_builder_class = LabelFormBuilder
    form_page_class = LabelFormPage
    submission_list_view_class = LabelSubmissionsListView


__all__ = [
    "Label",
    "LabelFormBlock",
    "LabelFormBuilder",
    "LabelFormPage",
    "LabelSubmissionsListView",
]
