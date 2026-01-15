"""View classes for the Nav Buttons plugin."""

from django.utils.translation import gettext as __

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.widgets.button import HeaderButton
from wagtail.models import Page

from wagtail_form_plugins.streamfield.dicts import SubmissionContextData
from wagtail_form_plugins.streamfield.views import StreamFieldSubmissionsListView


class NavButtonsSubmissionsListView(StreamFieldSubmissionsListView):
    """Customize lists submissions view, such as adding buttons on submission rows."""

    parent_form_page_class = Page

    def get_context_data(self, **kwargs) -> SubmissionContextData:
        """Alter submission context data to add buttons to the page header."""
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        finder = AdminURLFinder()
        form_index_page = self.parent_form_page_class.objects.first()

        context_data["header_buttons"] += [
            HeaderButton(
                label=__("Forms list"),
                url="/".join(str(finder.get_edit_url(form_index_page)).split("/")[:-2]),
                classname="forms-btn-secondary",
                icon_name="list-ul",
                priority=10,
            ),
            HeaderButton(
                label=__("View form"),
                url=self.form_page.url,
                classname="forms-btn-secondary",
                icon_name="view",
                attrs={"target": "_blank"},
                priority=20,
            ),
            HeaderButton(
                label=__("Edit form"),
                url=finder.get_edit_url(context_data["form_page"]),
                classname="forms-btn-primary",
                icon_name="edit",
                priority=30,
            ),
        ]

        return context_data
