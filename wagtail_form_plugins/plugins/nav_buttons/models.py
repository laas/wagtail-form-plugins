"""Models definition for the NavButtons form plugin."""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin.widgets.button import HeaderButton

from wagtail_form_plugins.streamfield.models import StreamFieldFormPage


class NavButtonsFormPage(StreamFieldFormPage):
    """A form page used to add navigation buttons in the form admin page."""

    def admin_header_buttons(self) -> list[HeaderButton]:
        """Add a button pointing to the list of submissions."""
        submissions_amount = self.form_submission_class.objects.filter(page=self).count()

        return [
            HeaderButton(
                label=_("{nb_subs} submission(s)").format(nb_subs=submissions_amount),
                url=reverse("wagtailforms:list_submissions", args=[self.pk]),
                classname="forms-btn-secondary",
                icon_name="list-ul",
                attrs={"disabled": True} if submissions_amount == 0 else {},
            ),
        ]

    class Meta:
        abstract = True
