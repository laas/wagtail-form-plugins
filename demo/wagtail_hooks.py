"""Wagtail hooks of the demo app - see https://docs.wagtail.org/en/stable/reference/hooks.html."""

from django.urls import reverse

from wagtail import hooks
from wagtail.admin.widgets import PageListingButton
from wagtail.contrib.forms.wagtail_hooks import FormsMenuItem

from wagtail_form_plugins import hooks as wfm_hooks

from .models import FormPage, CustomFormSubmission


hooks.register("insert_global_admin_css", wfm_hooks.templating_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.conditional_fields_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.emails_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.nav_buttons_admin_css)


@hooks.register("register_page_listing_buttons")
def page_listing_buttons(page, user, next_url=None):
    """Add a button on each row of the admin form list table to access the list of submissions."""
    if isinstance(page, FormPage):
        nb_results = CustomFormSubmission.objects.filter(page=page).count()
        yield PageListingButton(
            "no result" if nb_results == 0 else f"{ nb_results } results",
            reverse("wagtailforms:list_submissions", args=[page.pk]),
            priority=10,
            attrs={"disabled": "true"} if nb_results == 0 else {},
        )


@hooks.register("construct_main_menu")
def hide_old_form_menu_item(request, menu_items):
    """Hide the old form item from the main menu."""
    menu_items[:] = [mi for mi in menu_items if not isinstance(mi, FormsMenuItem)]
