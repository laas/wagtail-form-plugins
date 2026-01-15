"""Named form: add user value in form sumission, allowing to fill the form only once per user."""

from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import AuthFormPage, AuthFormSubmission
from .panels import UniqueResponseFieldPanel


class AuthForm(Plugin):
    """
    Named form plugin: add user identification functionality to the form.

    This allows to display it on form results and authorise a user to answer a form only once.
    """

    form_page_class = AuthFormPage
    form_submission_class = AuthFormSubmission


__all__ = [
    "AuthForm",
    "AuthFormPage",
    "AuthFormSubmission",
    "UniqueResponseFieldPanel",
]
