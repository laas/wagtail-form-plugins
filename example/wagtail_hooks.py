from django.contrib.auth.models import Permission

from wagtail import hooks

from wagtail_form_mixins.templating.wagtail_hooks import templating_admin_css
from wagtail_form_mixins.conditional_fields.wagtail_hooks import conditional_fields_admin_css
from wagtail_form_mixins.actions.wagtail_hooks import actions_admin_css


hooks.register("insert_global_admin_css", templating_admin_css)
hooks.register("insert_global_admin_css", conditional_fields_admin_css)
hooks.register("insert_global_admin_css", actions_admin_css)


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
