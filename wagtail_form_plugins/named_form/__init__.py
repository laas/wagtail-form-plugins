from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import AuthFormPage, AuthFormSubmission
from .panels import UniqueResponseFieldPanel


class AuthForm(Plugin):
    form_page_class = AuthFormPage
    form_submission_class = AuthFormSubmission


__all__ = [
    "AuthForm",
    "AuthFormPage",
    "AuthFormSubmission",
    "UniqueResponseFieldPanel",
]
