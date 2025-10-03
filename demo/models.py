"""Models definition for the demo app."""

import sys
from typing import Any, ClassVar, TextIO

from django.conf import settings
from django.contrib.auth.models import AbstractUser, AnonymousUser, Group, Permission, User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import OutputWrapper
from django.db import models
from django.forms import EmailField, ValidationError
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.forms.models import FormSubmission as WagtailFormSubmission
from wagtail.fields import RichTextField, StreamBlock, StreamField
from wagtail.models import GroupPagePermission, Page

from wagtail_form_plugins import (
    conditional_fields,
    editable,
    emails,
    file_input,
    indexed_results,
    label,
    named_form,
    nav_buttons,
    templating,
    token_validation,
)
from wagtail_form_plugins.utils import print_email

LocalBlocks = list[tuple[str, Any]] | None

FORM_GROUP_PREFIX = "form_moderator_"

DEFAULT_EMAILS = [
    {
        "recipient_list": "{author.email}",
        "subject": 'New entry for form "{form.title}"',
        "message": """Hello {author.full_name},
On {result.publish_date} at {result.publish_time}, the user {user.full_name} has submitted \
the form "{form.title}", with the following content:

{result.data}

Have a nice day.""",
    },
    {
        "recipient_list": "{user.email}",
        "subject": 'Confirmation of the submission of the form "{form.title}"',
        "message": """Hello {user.full_name},
You just submitted the form "{form.title}", with the following content:

{result.data}

The form author has been informed.
Have a nice day.""",
    },
]


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


class CustomTemplatingFormatter(templating.TemplatingFormatter):
    """Custom templating formatter used to personalize template formatting such as user template."""

    def __init__(self, context: dict[str, Any]):
        super().__init__(context)
        self.submission: CustomFormSubmission  # type: ignore

    def get_user_data(self, user: User) -> dict[str, str]:
        """Return a dict used to format template variables related to the form user or author."""
        user_data: dict[str, Any] = super().get_user_data(user)

        if isinstance(user, AnonymousUser):
            user_data["city"] = "-"
            if self.submission:
                user_data["email"] = self.submission.email
        else:
            user_data["city"] = str(getattr(user, "city", "")).lower()

        return user_data

    def get_result_data(self, formated_fields: dict[str, tuple[str, str]]) -> dict[str, str]:
        """Return a dict used to format template variables related to the form results."""
        result_data = super().get_result_data(formated_fields)
        if self.submission:
            result_data["index"] = str(self.submission.index)
        return result_data

    @classmethod
    def doc(cls) -> dict[str, dict[str, tuple[str, str]]]:
        """Return the dict used to build the template documentation."""
        doc = super().doc()
        doc["user"]["email"] = (__("the user email used for validation"), "alovelace@example.com")
        doc["user"]["city"] = (__("the form user city"), "Paris")
        doc["result"]["index"] = (__("the result index"), "42")
        return doc


class CustomFormBuilder(  # type: ignore
    label.LabelFormBuilder,
    file_input.FileInputFormBuilder,
    conditional_fields.ConditionalFieldsFormBuilder,
):
    """A custom form builder extended with some plugins to extend its features."""

    file_input_max_size = settings.FORMS_FILE_UPLOAD_MAX_SIZE


class CustomSubmissionListView(
    file_input.FileInputSubmissionsListView,
    nav_buttons.NavButtonsSubmissionsListView,
    conditional_fields.ConditionalFieldsSubmissionsListView,
):
    """A custom submission list view extended with some plugins to extend its features."""

    file_input_parent_page_class = FormIndexPage


class CustomValidationForm(token_validation.ValidationForm):
    """A small form with an email field, used to send validation email to access the actual form."""

    validation_email = EmailField(
        label="Confirmation de votre adresse mail / Mail address confirmation",
        max_length=100,
    )


class CustomEmailsToSendBlock(emails.EmailsFormBlock):
    """The custom Wagtail block used when configuring form emails behavior."""

    templating_formatter_class = CustomTemplatingFormatter

    def __init__(self, local_blocks: LocalBlocks = None, search_index: bool = True, **kwargs):
        templating.TemplatingFormBlock.add_help_messages(
            self.get_block_class().declared_blocks.values(),  # type: ignore
            ["subject", "message", "recipient_list", "reply_to"],
            self.templating_formatter_class.help(),
        )
        super().__init__(local_blocks, search_index, **kwargs)

    def get_block_class(self) -> type[StreamBlock]:
        """Return the block class."""
        return emails.EmailsFormBlock

    def validate_email(self, field_value: str) -> None:
        """Validate the email addresses field value."""
        try:
            if not self.templating_formatter_class.contains_template(field_value):
                super().validate_email(field_value)
        except ValueError as err:
            err_message = _("Wrong template syntax. See tooltip for a list of available keywords.")
            raise ValidationError(err_message) from err

    class Meta:  # type: ignore
        collapsed = True


class CustomFormSubmission(
    token_validation.TokenValidationFormSubmission,
    named_form.AuthFormSubmission,
    indexed_results.IndexedResultsFormSubmission,
):
    """A custom model for form submission, extended with mixins to extend its features"""

    def get_base_class(self) -> type[WagtailFormSubmission]:
        """Return the current class. Used by some submission classes to list object instances."""
        return self.__class__  # type: ignore

    class Meta:  # type: ignore
        pass


class CustomFormFieldsBlock(
    conditional_fields.ConditionalFieldsFormBlock,
    label.LabelFormBlock,
    file_input.FileInputFormBlock,
    templating.TemplatingFormBlock,
):
    """The custom Wagtail block used when adding fields to a form."""

    templating_formatter_class = CustomTemplatingFormatter

    class Meta:  # type: ignore
        pass


class CustomFormPage(  # type: ignore
    token_validation.TokenValidationFormPage,
    emails.EmailActionsFormPage,
    templating.TemplatingFormPage,
    file_input.FileInputFormPage,
    conditional_fields.ConditionalFieldsFormPage,
    named_form.AuthFormPage,
    nav_buttons.NavButtonsFormPage,
    indexed_results.IndexedResultsFormPage,
    editable.EditableFormPage,
):
    """A custom abstract form page model extended with some plugins to extend its features."""

    parent_page_type: ClassVar = ["demo.FormIndexPage"]
    subpage_types: ClassVar = []

    validation_form_class = CustomValidationForm
    submissions_list_view_class = CustomSubmissionListView

    file_input_upload_dir = "demo_forms_uploads/%Y/%m/%d"
    templating_formatter_class = CustomTemplatingFormatter
    token_validation_from_email = settings.FORMS_FROM_EMAIL
    token_validation_reply_to: ClassVar = [settings.FORMS_FROM_EMAIL]
    token_validation_expiration_delay = settings.FORMS_VALIDATION_EXPIRATION_DELAY

    def get_group_name(self) -> str:
        """Return the name of the form admin user group."""
        return f"{FORM_GROUP_PREFIX}{self.slug}"

    def get_submission_class(self) -> type[WagtailFormSubmission]:
        """Return the custom form submission model class."""
        return CustomFormSubmission  # type: ignore

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Serve the form page."""
        response = super().serve(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect) or not response.context_data:
            return response

        response.context_data["page"].outro = settings.FORMS_RGPD_TEXT.strip()
        return response

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
        if self.owner:
            self.owner.groups.add(form_admins)

        return result

    def delete(self, *args, **kwargs) -> Any:
        """Delete the form."""
        result = super().delete(*args, **kwargs)
        Group.objects.get(name=self.get_group_name()).delete()
        return result

    def set_page_permissions(self, group: Group, permissions_name: list[str]) -> None:
        """Set user permissions of the form page."""
        for permission_name in permissions_name:
            permission = Permission.objects.get(codename=f"{permission_name}_page")
            GroupPagePermission.objects.get_or_create(group=group, page=self, permission=permission)

    class Meta:  # type: ignore
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
        default=[emails.email_to_block(email) for email in DEFAULT_EMAILS],
        blank=True,
    )

    content_panels: ClassVar = [
        *CustomFormPage.content_panels,
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        token_validation.TokenValidationFieldPanel(),
        FieldPanel("emails_to_send"),
        named_form.UniqueResponseFieldPanel(),
    ]
