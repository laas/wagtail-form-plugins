"""Models definition for the NavButtons form plugin."""

from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from wagtail.admin.widgets.button import HeaderButton

from wagtail_form_plugins.base.models import FormMixin


class NavButtonsFormMixin(FormMixin):
    """A mixin used to add navigation buttons in the form admin page."""

    def admin_header_buttons(self):
        """Add a button pointing to the list of submissions."""
        submissions_amount = self.get_submission_class().objects.filter(page=self).count()

        return [
            HeaderButton(
                label=_("{nb_subs} submission(s)").format(nb_subs=submissions_amount),
                url=reverse("wagtailforms:list_submissions", args=[self.pk]),
                classname="forms-btn-secondary",
                icon_name="list-ul",
                attrs={"disabled": True} if submissions_amount == 0 else {},
            )
        ]

    class Meta:
        abstract = True
