from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import TokenValidationFormPage, TokenValidationFormSubmission, ValidationForm
from .panels import TokenValidationFieldPanel


class TokenValidation(Plugin):
    form_page_class = TokenValidationFormPage
    form_submission_class = TokenValidationFormSubmission


__all__ = [
    "TokenValidation",
    "TokenValidationFieldPanel",
    "TokenValidationFormPage",
    "TokenValidationFormSubmission",
    "ValidationForm",
]
