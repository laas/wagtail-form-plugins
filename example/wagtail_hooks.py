from django.contrib.auth.models import Permission
from django.urls import reverse

from wagtail import hooks
from wagtail.admin.widgets import PageListingButton
from wagtail.contrib.forms.wagtail_hooks import FormsMenuItem

from wagtail_form_mixins import hooks as wfm_hooks

from .models import FormPage, CustomFormSubmission


hooks.register("insert_global_admin_css", wfm_hooks.templating_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.conditional_fields_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.emails_admin_css)
hooks.register("insert_global_admin_css", wfm_hooks.nav_buttons_admin_css)


def permissions(app, model):
    return Permission.objects.filter(
        content_type__app_label=app,
        codename__in=[f"view_{model}", f"add_{model}", f"change_{model}", f"delete_{model}"],
    )


@hooks.register("register_permissions")
def formpage_permissions():
    return permissions("example", "formpage")


@hooks.register("register_permissions")
def formindexpage_permissions():
    return permissions("example", "formindexpage")


@hooks.register("register_permissions")
def formsubmission_permissions():
    return permissions("example", "customformsubmission")


@hooks.register("filter_form_submissions_for_user")
def construct_forms_for_user(user, queryset):
    if not user.is_superuser:
        queryset = queryset.none()

    return queryset


@hooks.register("register_page_listing_buttons")
def page_listing_buttons(page, user, next_url=None):
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
    menu_items[:] = [mi for mi in menu_items if not isinstance(mi, FormsMenuItem)]
