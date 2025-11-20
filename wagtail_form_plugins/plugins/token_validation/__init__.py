"""Token Validation plugin: add token-validation process via email, useful for public forms."""

from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import ValidationForm, ValidationFormPage, ValidationFormSubmission
from .panels import ValidationFieldPanel


class Validation(Plugin):
    """Token Validation plugin: add token-validation process via email, useful for public forms."""

    form_page_class = ValidationFormPage
    form_submission_class = ValidationFormSubmission


__all__ = [
    "Validation",
    "ValidationFieldPanel",
    "ValidationForm",
    "ValidationFormPage",
    "ValidationFormSubmission",
]
