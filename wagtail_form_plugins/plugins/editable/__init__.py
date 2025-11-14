from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import EditableFormPage


class Editable(Plugin):
    form_page_class = EditableFormPage


__all__ = [
    "Editable",
    "EditableFormPage",
]
