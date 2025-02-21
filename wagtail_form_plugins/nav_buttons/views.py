"""View classes for the Nav Buttons plugin."""

from django.utils.translation import gettext_lazy as _

from wagtail.admin.widgets.button import HeaderButton
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.contrib.forms.views import SubmissionsListView


class NavButtonsSubmissionsListView(SubmissionsListView):
    """Customize lists submissions view, such as adding buttons on submission rows."""

    def get_context_data(self, **kwargs):
        """Return context for view"""
        context_data = super().get_context_data(**kwargs)

        if self.is_export:
            return context_data

        finder = AdminURLFinder()
        form_index_page = self.form_parent_page_model.objects.first()

        context_data["header_buttons"] += [
            HeaderButton(
                label=_("Forms list"),
                url="/".join(finder.get_edit_url(form_index_page).split("/")[:-2]),
                classname="forms-btn-secondary",
                icon_name="list-ul",
                priority=10,
            ),
            HeaderButton(
                label=_("View form"),
                url=self.form_page.url,
                classname="forms-btn-secondary",
                icon_name="view",
                attrs={"target": "_blank"},
                priority=20,
            ),
            HeaderButton(
                label=_("Edit form"),
                url=finder.get_edit_url(context_data["form_page"]),
                classname="forms-btn-primary",
                icon_name="edit",
                priority=30,
            ),
        ]

        return context_data
