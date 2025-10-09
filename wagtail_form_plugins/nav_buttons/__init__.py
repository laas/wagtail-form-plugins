from wagtail_form_plugins.streamfield.plugin import Plugin

from .hooks import hook_nav_buttons_admin_css
from .models import NavButtonsFormPage
from .views import NavButtonsSubmissionsListView


class NavButtons(Plugin):
    form_page_class = NavButtonsFormPage
    submission_list_view_class = NavButtonsSubmissionsListView


__all__ = [
    "NavButtons",
    "NavButtonsFormPage",
    "NavButtonsSubmissionsListView",
    "hook_nav_buttons_admin_css",
]
