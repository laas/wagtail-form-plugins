from django.utils.translation import gettext_lazy as _

from wagtail.admin.widgets.button import HeaderButton
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.contrib.forms.views import SubmissionsListView


class NavButtonsSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        finder = AdminURLFinder()
        context_data = super().get_context_data(**kwargs)
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
                label=_("Edit form"),
                url=finder.get_edit_url(context_data["form_page"]),
                classname="forms-btn-primary",
                icon_name="edit",
                priority=20,
            ),
        ]

        return context_data
