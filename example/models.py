import sys

from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.models import FormMixin
from wagtail.models import Page

from wagtail_form_mixins import models as wfm_models
from wagtail_form_mixins import blocks as wfm_blocks
from wagtail_form_mixins import panels as wfm_panels
from wagtail_form_mixins import views as wfm_views
from wagtail_form_mixins import forms as wfm_forms

from wagtail_form_mixins.templating.formatter import TEMPLATE_VAR_LEFT, TEMPLATE_VAR_RIGHT

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
    form_title = models.CharField(
        max_length=255,
        verbose_name=_("Form title"),
        help_text=_("A generic title displayed on all form pages."),
        default=_("Wagtail forms"),
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("intro"),
        FieldPanel("form_title"),
    ]

    parent_page_type = ["example.HomePage"]
    subpage_types = ["example.FormPage"]
    max_count = 1
    admin_default_ordering = "ord"

    @staticmethod
    def create_if_missing(stdout=sys.stdout):
        if FormIndexPage.objects.first() is not None:
            return

        stdout.write("creating form index page")

        home, _ = Page.objects.get_or_create(slug="home")

        forms_index_page = FormIndexPage(
            title="Formulaires",
            slug="formulaires",
            depth=home.depth + 1,
            locale_id=home.locale_id,
        )
        home.add_child(instance=forms_index_page)
        return forms_index_page


class CustomTemplatingFormatter(wfm_models.TemplatingFormatter):
    def load_user_data(self, user: CustomUser):
        return {
            **super().load_user_data(user),
            "city": user.city.lower(),
        }

    @classmethod
    def doc(cls):
        doc = super().doc()
        doc["user"]["city"] = (_("the form user city"), "Paris")
        return doc


class CustomFormSubmission(wfm_models.NamedFormSubmission):
    pass


class CustomFormBuilder(
    wfm_forms.FileInputFormBuilder,
    wfm_forms.StreamFieldFormBuilder,
    wfm_forms.DatePickersFormBuilder,
):
    file_input_allowed_extensions = ["pdf", "jpg", "jpeg", "png"]


class CustomSubmissionListView(
    wfm_views.NamedSubmissionsListView,
    wfm_views.FileInputSubmissionsListView,
    wfm_views.NavButtonsSubmissionsListView,
):
    form_parent_page_model = FormIndexPage


class FileInput(wfm_models.AbstractFileInput):
    file = models.FileField(upload_to="example_forms/%Y/%m/%d")


class AbstractFormPage(
    wfm_models.EmailActionsFormMixin,
    wfm_models.TemplatingFormMixin,
    wfm_models.FileInputFormMixin,
    wfm_models.ConditionalFieldsFormMixin,
    wfm_models.NamedFormMixin,
    wfm_models.StreamFieldFormMixin,
    wfm_models.NavButtonsFormMixin,
    FormMixin,
    Page,
):
    template_context_class = CustomTemplatingFormatter
    form_builder = CustomFormBuilder
    file_input_model = FileInput
    submissions_list_view_class = CustomSubmissionListView
    parent_page_type = ["example.FormIndexPage"]
    subpage_types = []

    def get_submission_class(self):
        return CustomFormSubmission

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        response.context_data["page"].super_title = self.get_parent().form_title
        return response

    class Meta:
        abstract = True


class FormFieldsBlock(
    wfm_blocks.ConditionalFieldsFormBlock,
    wfm_blocks.FileInputFormBlock,
    wfm_blocks.TemplatingFormBlock,
    wfm_blocks.StreamFieldFormBlock,
):
    templating_formatter = CustomTemplatingFormatter


class EmailsToSendBlock(
    wfm_blocks.TemplatingEmailFormBlock,
    wfm_blocks.EmailsFormBlock,
):
    templating_formatter = CustomTemplatingFormatter

    def get_block_class(self):
        return wfm_blocks.EmailsFormBlock

    def validate_email(self, field_value):
        for key, example in CustomTemplatingFormatter.examples().items():
            field_value = field_value.replace(key, example)

        if TEMPLATE_VAR_LEFT in field_value or TEMPLATE_VAR_RIGHT in field_value:
            raise ValidationError(
                _("Unrecognized template keyword. See tooltip for a list of available keywords.")
            )

        super().validate_email(field_value)


class FormPage(AbstractFormPage):
    intro = RichTextField(
        blank=True,
        verbose_name=_("Form introduction text"),
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name=_("Text displayed after form submission"),
        default=_("Thank you!"),
    )
    form_fields = StreamField(
        FormFieldsBlock(),
        verbose_name=_("Form fields"),
    )
    outro = RichTextField(
        blank=True,
        verbose_name=_("Form conclusion text"),
        default=_(
            "Data collected in this form is stored by the IT team in order to process your request."
        ),
    )
    emails_to_send = StreamField(
        EmailsToSendBlock(),
        verbose_name=_("E-mails to send after form submission"),
        default=[wfm_blocks.email_to_block(email) for email in DEFAULT_EMAILS],
    )

    content_panels = [
        *AbstractFormPage.content_panels,
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("outro"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
        wfm_panels.UniqueResponseFieldPanel(),
    ]
