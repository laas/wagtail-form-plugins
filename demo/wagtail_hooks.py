"""Wagtail hooks of the demo app - see https://docs.wagtail.org/en/stable/reference/hooks.html."""

from collections.abc import Generator
from typing import Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.widgets.button import ListingButton
from wagtail.contrib.forms.wagtail_hooks import FormsMenuItem
from wagtail.models import Page

from demo.models import CustomFormSubmission, FormPage
from wagtail_form_plugins import conditional_fields, emails, nav_buttons, templating

hooks.register("insert_global_admin_css", templating.hook_templating_admin_css)
hooks.register("insert_global_admin_css", conditional_fields.hook_conditional_fields_admin_css)
hooks.register("insert_global_admin_css", emails.hook_emails_admin_css)
hooks.register("insert_global_admin_css", nav_buttons.hook_nav_buttons_admin_css)


@hooks.register("register_page_listing_buttons")  # type: ignore[ reportOptionalCall]
def page_listing_buttons(
    page: Page,
    _user: User,
    _next_url: str | None = None,
) -> Generator[ListingButton, Any, None]:
    """Add a button on each row of the admin form list table to access the list of submissions."""
    if isinstance(page, FormPage):
        nb_results = CustomFormSubmission.objects.filter(page=page).count()
        yield ListingButton(
            "no result" if nb_results == 0 else f"{nb_results} results",
            reverse("wagtailforms:list_submissions", args=[page.pk]),
            priority=10,
            attrs={"disabled": "true"} if nb_results == 0 else {},
        )


@hooks.register("construct_main_menu")  # type: ignore[ reportOptionalCall]
def hide_old_form_menu_item(_request: HttpRequest, menu_items: list[MenuItem]) -> None:
    """Hide the old form item from the main menu."""
    menu_items[:] = [mi for mi in menu_items if not isinstance(mi, FormsMenuItem)]
