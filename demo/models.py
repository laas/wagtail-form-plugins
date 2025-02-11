import sys
from typing import Any

from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, AnonymousUser
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.forms.models import FormMixin
from wagtail.models import Page, GroupPagePermission

from wagtail_form_plugins import models as wfp_models
from wagtail_form_plugins import blocks as wfp_blocks
from wagtail_form_plugins import panels as wfp_panels
from wagtail_form_plugins import views as wfp_views
from wagtail_form_plugins import forms as wfp_forms

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


class CustomUser(AbstractUser):
    city = models.CharField(max_length=255, verbose_name=_("City"))


class FormIndexPage(Page):
    PAGINATION = 15

    intro = RichTextField(
        verbose_name=_("Form index page introduction"),
        help_text=_("A rich text introduction to be displayed before the list of forms."),
        blank=True,
        default=_("Forms list"),
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("intro"),
    ]

    parent_page_type = ["demo.HomePage"]
    subpage_types = ["demo.FormPage"]
    max_count = 1
    admin_default_ordering = "ord"

    def admin_header_buttons(self):
        return [
            HeaderButton(
                label=_("Forms list"),
                url=reverse("wagtailadmin_explore", args=[self.pk]),
                classname="forms-btn-primary",
                icon_name="list-ul",
            )
        ]

    @staticmethod
    def create_if_missing(home_page: Page, stdout=sys.stdout):
        if FormIndexPage.objects.first() is not None:
            return

        stdout.write("creating form index page")

        forms_index_page = FormIndexPage(
            title="Formulaires",
            slug="formulaires",
            depth=home_page.depth + 1,
            locale_id=home_page.locale_id,
        )
        home_page.add_child(instance=forms_index_page)
        return forms_index_page


class CustomTemplatingFormatter(wfp_models.TemplatingFormatter):
    def get_user_data(self, user: CustomUser):
        user_data: dict[str, Any] = super().get_user_data(user)
        is_anonymous = isinstance(user, AnonymousUser)

        if is_anonymous and self.submission:
            user_data["email"] = self.submission.email
        user_data["city"] = "-" if is_anonymous else user.city.lower()

        return user_data

    def get_result_data(self, formated_fields):
        return {
            **super().get_result_data(formated_fields),
            "index": str(self.submission.index),
        }

    @classmethod
    def doc(cls):
        doc = super().doc()
        doc["user"]["email"] = (_("the user email used for validation"), "alovelace@example.com")
        doc["user"]["city"] = (_("the form user city"), "Paris")
        doc["result"]["index"] = (_("the result index"), "42")
        return doc


class CustomFormSubmission(
    wfp_models.TokenValidationSubmission,
    wfp_models.NamedFormSubmission,
    wfp_models.IndexedResultsSubmission,
):
    def get_base_class(self):
        return self.__class__


class CustomFormBuilder(
    wfp_forms.FileInputFormBuilder,
    wfp_forms.StreamFieldFormBuilder,
    wfp_forms.DatePickersFormBuilder,
):
    file_input_max_size = settings.FORMS_FILE_UPLOAD_MAX_SIZE


class CustomSubmissionListView(
    wfp_views.FileInputSubmissionsListView,
    wfp_views.NavButtonsSubmissionsListView,
    wfp_views.ConditionalFieldsSubmissionsListView,
):
    form_parent_page_model = FormIndexPage


class FileInput(wfp_models.AbstractFileInput):
    upload_dir = "demo_forms_uploads/%Y/%m/%d"


class AbstractFormPage(
    wfp_models.TokenValidationFormMixin,
    wfp_models.EmailActionsFormMixin,
    wfp_models.TemplatingFormMixin,
    wfp_models.FileInputFormMixin,
    wfp_models.ConditionalFieldsFormMixin,
    wfp_models.NamedFormMixin,
    wfp_models.StreamFieldFormMixin,
    wfp_models.NavButtonsFormMixin,
    wfp_models.IndexedResultsFormMixin,
    wfp_models.EditableFormMixin,
    FormMixin,
    Page,
):
    formatter_class = CustomTemplatingFormatter
    form_builder = CustomFormBuilder
    file_input_model = FileInput
    submissions_list_view_class = CustomSubmissionListView
    parent_page_type = ["demo.FormIndexPage"]
    subpage_types = []

    def get_group_name(self):
        return f"{ FORM_GROUP_PREFIX }{ self.slug }"

    def get_submission_class(self):
        return CustomFormSubmission

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)

        if isinstance(response, HttpResponseRedirect):
            return response

        response.context_data["page"].outro = settings.FORMS_RGPD_TEXT.strip()
        return response

    def send_email(self, email: dict):
        """Used in local development to avoid to actually send a mail."""
        if settings.DEBUG and not settings.FORMS_DEV_SEND_MAIL:
            print("=== sending email ===")
            for k, v in email.items():
                print(f"{ k }: { v }")
        else:
            super().send_email(email)

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        super().save(clean, user, log_action, **kwargs)
        form_admins, _ = Group.objects.get_or_create(name=self.get_group_name())
        self.set_page_permissions(form_admins, ["publish", "change", "lock", "unlock"])
        if self.owner:
            self.owner.groups.add(form_admins)

        # to make forms private:
        # PageViewRestriction.objects.get_or_create(page=self, restriction_type="login")

    def delete(self, *args, **kwargs):
        Group.objects.get(name=self.get_group_name()).delete()
        return super().delete(*args, **kwargs)

    def set_page_permissions(self, group, permissions_name):
        for permission_name in permissions_name:
            permission = Permission.objects.get(codename=f"{ permission_name }_page")
            GroupPagePermission.objects.get_or_create(group=group, page=self, permission=permission)

    class Meta:
        abstract = True


class FormFieldsBlock(
    wfp_blocks.ConditionalFieldsFormBlock,
    wfp_blocks.FileInputFormBlock,
    wfp_blocks.TemplatingFormBlock,
    wfp_blocks.StreamFieldFormBlock,
):
    formatter_class = CustomTemplatingFormatter


class EmailsToSendBlock(wfp_blocks.EmailsFormBlock):
    formatter_class = CustomTemplatingFormatter

    def __init__(self, local_blocks=None, search_index=True, **kwargs):
        wfp_blocks.TemplatingFormBlock.add_help_messages(
            self.get_block_class().declared_blocks.values(),
            ["subject", "message", "recipient_list", "reply_to"],
            self.formatter_class.help(),
        )
        super().__init__(local_blocks, search_index, **kwargs)

    def get_block_class(self):
        return wfp_blocks.EmailsFormBlock

    def validate_email(self, field_value: str) -> None:
        try:
            if not self.formatter_class.contains_template(field_value):
                super().validate_email(field_value)
        except ValueError as err:
            err_message = _("Wrong template syntax. See tooltip for a list of available keywords.")
            raise ValidationError(err_message) from err

    class Meta:
        collapsed = True


class FormPage(AbstractFormPage):
    intro = RichTextField(
        verbose_name=_("Form introduction text"),
        blank=True,
    )
    form_fields = StreamField(
        FormFieldsBlock(),
        verbose_name=_("Form fields"),
        blank=True,
    )
    thank_you_text = RichTextField(
        verbose_name=_("Text displayed after form submission"),
        default=_("Thank you!"),
        blank=True,
    )
    validation_title = models.CharField(
        verbose_name=_("E-mail title"),
        default=_("User validation required to fill a public form"),
        max_length=100,
    )
    validation_body = RichTextField(
        verbose_name=_("E-mail content"),
        default=_("Please click on the following link to fill the form: {validation_url} ."),
    )
    emails_to_send = StreamField(
        EmailsToSendBlock(),
        verbose_name=_("E-mails to send after form submission"),
        default=[wfp_blocks.email_to_block(email) for email in DEFAULT_EMAILS],
        blank=True,
    )

    content_panels = [
        *AbstractFormPage.content_panels,
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldPanel("validation_title"),
                FieldPanel("validation_body"),
            ],
            "Validation e-mail",
        ),
        FieldPanel("emails_to_send"),
        wfp_panels.UniqueResponseFieldPanel(),
    ]
