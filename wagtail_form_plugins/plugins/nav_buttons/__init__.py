"""Nav buttons plugin: add some buttons for an easier novigation for form admins."""

from django.templatetags.static import static
from django.utils.html import format_html

from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import NavButtonsFormPage
from .views import NavButtonsSubmissionsListView


class NavButtons(Plugin):
    """Nav buttons plugin: add some buttons for an easier novigation for form admins."""

    form_page_class = NavButtonsFormPage
    submission_list_view_class = NavButtonsSubmissionsListView

    @classmethod
    def get_injected_admin_css(cls) -> str:
        """Return the css to inject in the form admin page when using the Nav buttons plugin."""
        return format_html(
            '<link rel="stylesheet" href="{href}">',
            href=static("wagtail_form_plugins/nav_buttons/css/form_admin.css"),
        )


__all__ = [
    "NavButtons",
    "NavButtonsFormPage",
    "NavButtonsSubmissionsListView",
]
