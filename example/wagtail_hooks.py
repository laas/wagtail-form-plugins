from wagtail import hooks

from wagtail_form_mixins.templating.wagtail_hooks import templating_admin_css
from wagtail_form_mixins.conditional_fields.wagtail_hooks import conditional_fields_admin_css
from wagtail_form_mixins.actions.wagtail_hooks import actions_admin_css


hooks.register("insert_global_admin_css", templating_admin_css)
hooks.register("insert_global_admin_css", conditional_fields_admin_css)
hooks.register("insert_global_admin_css", actions_admin_css)
