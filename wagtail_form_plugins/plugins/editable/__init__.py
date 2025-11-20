"""Editable plugin: allow form admins to modify form submissions."""

from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import EditableFormPage


class Editable(Plugin):
    """Editable plugin: allow form admins to modify form submissions."""

    form_page_class = EditableFormPage


__all__ = [
    "Editable",
    "EditableFormPage",
]
