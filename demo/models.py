"""Models definition for the demo app."""

import sys
from typing import Any, ClassVar, TextIO

from django.conf import settings
from django.contrib.auth.models import AbstractUser, AnonymousUser, Group, Permission, User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import OutputWrapper
from django.db import models
from django.forms import EmailField
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.admin.widgets.button import HeaderButton
from wagtail.fields import RichTextField, StreamField
from wagtail.models import GroupPagePermission, Page

from wagtail_form_plugins import plugins
from wagtail_form_plugins.plugins.emails.blocks import EmailsFormBlock, email_to_block
from wagtail_form_plugins.plugins.emails.dicts import EmailsToSendBlockDict
from wagtail_form_plugins.streamfield.plugin import WagtailFormPlugin
from wagtail_form_plugins.utils import LocalBlocks, print_email

from modelcluster.fields import ParentalManyToManyField
from wagtailautocomplete.edit_handlers import AutocompletePanel

FORM_GROUP_PREFIX = "form_moderator_"

DEFAULT_EMAILS: list[EmailsToSendBlockDict] = [
    {
        "recipient_list": "{author.email}",
        "from_email": "",
        "reply_to": "",
        "subject": 'New entry for form "{form.title}"',
        "message": """Hello {author.full_name},
On {result.publish_date} at {result.publish_time}, the user {user.full_name} has submitted \
the form "{form.title}", with the following content:

{result.data}

Have a nice day.""",
    },
    {
        "recipient_list": "{user.email}",
        "from_email": "",
        "reply_to": "",
        "subject": 'Confirmation of the submission of the form "{form.title}"',
        "message": """Hello {user.full_name},
You just submitted the form "{form.title}", with the following content:

{result.data}

The form author has been informed.
Have a nice day.""",
    },
]


# Form plugins definition. Comment a line to disable the corresponding plugin.
wfp = WagtailFormPlugin(
    plugins.ConditionalFields,
    plugins.Editable,
    plugins.EmailActions,
    plugins.FileInput,
    plugins.IndexedResults,
    plugins.Label,
    plugins.AuthForm,
    plugins.NavButtons,
    plugins.Templating,
    plugins.Validation,
)


class FormIndexPage(Page):
    """A page used to manage forms in the Wagtail admin page and list them in the published page."""

    PAGINATION = 15

    intro = RichTextField(
        verbose_name=_("Form index page introduction"),
        help_text=_("A rich text introduction to be displayed before the list of forms."),
        blank=True,
        default=_("Forms list"),
    )

    content_panels: ClassVar = [
        *Page.content_panels,
        FieldPanel("intro"),
    ]

    parent_page_type: ClassVar = ["demo.HomePage"]
    subpage_types: ClassVar = ["demo.FormPage"]
    max_count = 1
    admin_default_ordering = "ord"

    def admin_header_buttons(self) -> list[HeaderButton]:
        """Add a button on the page header used to go to the list of forms."""
        return [
            HeaderButton(
                label=__("Forms list"),
                url=reverse("wagtailadmin_explore", args=[self.pk]),
                classname="forms-btn-primary",
                icon_name="list-ul",
            ),
        ]

    @staticmethod
    def create_if_missing(
        home_page: Page,
        stdout: TextIO | OutputWrapper = sys.stdout,
    ) -> Page | None:
        """Create the index page if there is none."""
        if FormIndexPage.objects.first() is not None:
            return None

        stdout.write("creating form index page")

        forms_index_page = FormIndexPage(
            title="Formulaires",
            slug="formulaires",
            depth=home_page.depth + 1,
            locale_id=home_page.locale.id,
        )
        home_page.add_child(instance=forms_index_page)
        return forms_index_page


class CustomUser(AbstractUser):
    """A custom user model."""

    city = models.CharField(max_length=255, verbose_name=_("City"))


class CustomTemplatingFormatter(plugins.templating.TemplatingFormatter):
    """Custom templating formatter used to personalize template formatting such as user template."""

    def get_user_data(self, user: User) -> plugins.templating.UserDataDict:
        """Return a dict used to format template variables related to the form user or author."""
        user_data = super().get_user_data(user)

        if isinstance(user, AnonymousUser):
            user_data["city"] = "-"  # type: ignore[invalid-key]
            if self.submission:
                user_data["email"] = self.submission.email  # type: ignore[possibly-missing-attribute]
        else:
            user_data["city"] = getattr(user, "city", "").lower()  # type: ignore[invalid-key]

        return user_data

    def get_result_data(
        self,
        formated_fields: dict[str, tuple[str, str]],
    ) -> plugins.templating.ResultDataDict | None:
        """Return a dict used to format template variables related to the form results."""
        result_data = super().get_result_data(formated_fields)
        if result_data:
            result_data["index"] = self.submission.index  # type: ignore[possibly-missing-attribute]
        return result_data

    @classmethod
    def doc(cls) -> dict[str, dict[str, tuple[str, str]]]:
        """Return the dict used to build the template documentation."""
        doc = super().doc()
        doc["user"]["email"] = (__("the user email used for validation"), "alovelace@example.com")
        doc["user"]["city"] = (__("the form user city"), "Paris")
        doc["result"]["index"] = (__("the result index"), "42")
        return doc


class CustomFormBuilder(*wfp.form_builder_classes):
    """A custom form builder extended with some plugins to extend its features."""

    file_input_max_size = settings.FORMS_FILE_UPLOAD_MAX_SIZE


class CustomSubmissionListView(*wfp.submission_list_view_classes):
    """A custom submission list view extended with some plugins to extend its features."""

    parent_form_page_class = FormIndexPage


class CustomValidationForm(plugins.token_validation.ValidationForm):
    """A small form with an email field, used to send validation email to access the actual form."""

    validation_email = EmailField(
        label="Confirmation de votre adresse mail / Mail address confirmation",
        max_length=100,
    )


class CustomEmailsToSendBlock(EmailsFormBlock):
    """The custom Wagtail block used when configuring form emails behavior."""

    templating_formatter_class = CustomTemplatingFormatter

    def __init__(self, local_blocks: LocalBlocks = None, *, search_index: bool = True, **kwargs):
        super().__init__(local_blocks, search_index, **kwargs)
        plugins.templating.TemplatingFormBlock.add_help_messages(
            self.child_blocks.values(),
            ["subject", "message", "recipient_list", "reply_to"],
        )

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        collapsed = True


class CustomFormSubmission(*wfp.form_submission_classes):
    """A custom model for form submission, extended with mixins to extend its features."""


class CustomFormFieldsBlock(*wfp.form_block_classes):
    """The custom Wagtail block used when adding fields to a form."""

    templating_formatter_class = CustomTemplatingFormatter


class CustomFormField(*wfp.form_field_classes):
    """A custom form field extending form field features from all plugins."""


class CustomFormPage(*wfp.form_page_classes):
    """A custom abstract form page model extended with some plugins to extend its features."""

    parent_page_type: ClassVar = ["demo.FormIndexPage"]
    subpage_types: ClassVar = []

    form_builder_class = CustomFormBuilder
    form_submission_class = CustomFormSubmission
    submissions_list_view_class = CustomSubmissionListView
    form_field_class = CustomFormField

    file_input_upload_dir = "demo_forms_uploads/%Y/%m/%d"
    templating_formatter_class = CustomTemplatingFormatter
    token_validation_form_class = CustomValidationForm
    token_validation_from_email = settings.FORMS_FROM_EMAIL
    token_validation_reply_to: ClassVar = [settings.FORMS_FROM_EMAIL]
    token_validation_expiration_delay = settings.FORMS_VALIDATION_EXPIRATION_DELAY

    def get_group_name(self) -> str:
        """Return the name of the form admin user group."""
        return f"{FORM_GROUP_PREFIX}{self.slug}"

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        """Update context to modify page outro."""
        context = super().get_context(request)
        context["page"].outro = settings.FORMS_RGPD_TEXT.strip()
        return context

    def send_action_email(self, email: EmailMultiAlternatives) -> None:
        """Print the action e-mail instead sending it when debugging."""
        if settings.DEBUG and not settings.FORMS_DEV_SEND_MAIL:
            print_email(email)
        else:
            email.send()

    def send_validation_email(self, email: EmailMultiAlternatives) -> None:
        """Print the validation e-mail instead sending it when debugging."""
        if settings.DEBUG and not settings.FORMS_DEV_SEND_MAIL:
            print_email(email)
        else:
            email.send()

    def save(self, *args, **kwargs) -> None:
        """Save the form."""
        result = super().save(*args, **kwargs)

        form_admins, _ = Group.objects.get_or_create(name=self.get_group_name())
        self.set_page_permissions(form_admins, ["publish", "change", "lock", "unlock"])

        old_admins = CustomUser.objects.filter(groups=form_admins)
        new_admins = CustomUser.objects.filter(formpage=self)

        if self.owner and self.owner not in old_admins:
            self.owner.groups.add(form_admins)

        for new_admin in new_admins:
            if new_admin not in old_admins and new_admin != self.owner:
                new_admin.groups.add(form_admins)

        for old_admin in old_admins:
            if old_admin not in new_admins:
                old_admin.groups.remove(form_admins)

        return result

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        """Delete the form."""
        result = super().delete(*args, **kwargs)
        Group.objects.get(name=self.get_group_name()).delete()
        return result

    def set_page_permissions(self, group: Group, permissions_name: list[str]) -> None:
        """Set user permissions of the form page."""
        group.permissions.add(Permission.objects.get(codename="access_admin"))
        for permission_name in permissions_name:
            permission = Permission.objects.get(codename=f"{permission_name}_page")
            GroupPagePermission.objects.get_or_create(group=group, page=self, permission=permission)

    class Meta:
        abstract = True


class FormPage(CustomFormPage):
    """The actual form page model."""

    intro = RichTextField(
        verbose_name=_("Form introduction text"),
        blank=True,
    )
    form_fields = StreamField(
        CustomFormFieldsBlock(),
        verbose_name=_("Form fields"),
        blank=True,
    )
    thank_you_text = RichTextField(
        verbose_name=_("Text displayed after form submission"),
        default=_("Thank you!"),
        blank=True,
    )
    emails_to_send = StreamField(
        CustomEmailsToSendBlock(),
        verbose_name=_("E-mails to send after form submission"),
        default=[email_to_block(email) for email in DEFAULT_EMAILS],
        blank=True,
    )
    administrators = ParentalManyToManyField(
        CustomUser,
        verbose_name=_("administrators"),
        blank=True,
    )

    content_panels: ClassVar = [
        *CustomFormPage.content_panels,
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        plugins.token_validation.ValidationFieldPanel(),
        FieldPanel("emails_to_send"),
        AutocompletePanel("administrators"),
        plugins.named_form.UniqueResponseFieldPanel(),
    ]
