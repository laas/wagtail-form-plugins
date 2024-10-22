from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import FormMixin
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from wagtail_form_mixins import models as wfm_models
from wagtail_form_mixins import blocks as wfm_blocks
from wagtail_form_mixins import panels as wfm_panels
from wagtail_form_mixins import views as wfm_views


DEFAULT_EMAILS = [
    {
        "recipient_list": "{author.email}",
        "subject": 'Nouvelle entrée pour le formulaire "{form.title}"',
        "message": """Bonjour {author.full_name},
Le {result.publish_date} à {result.publish_time}, l’utilisateur {user.full_name} a complété le \
formulaire "{form.title}", avec le contenu suivant:

{result.data}

Bonne journée.""",
    },
    {
        "recipient_list": "{user.email}",
        "subject": 'Confirmation de l’envoi du formulaire "{form.title}"',
        "message": """Bonjour {user.full_name},
Vous venez de compléter le formulaire "{form.title}", avec le contenu suivant:

{result.data}

L’auteur du formulaire en a été informé.
Bonne journée.""",
    },
]


@register_snippet
class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    panels = [
        FieldPanel("name"),
        FieldPanel("members"),
    ]

    def __str__(self) -> str:
        return str(self.name)


@register_snippet
class Service(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    panels = [
        FieldPanel("name"),
        FieldPanel("members"),
    ]

    def __str__(self) -> str:
        return str(self.name)


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


class CustomFormContext(wfm_models.FormContext):
    def format_user(self, user: User):
        user_dict = super().format_user(user)

        teams = [service.name for service in Team.objects.filter(members__pk=user.pk)]
        services = [service.name for service in Service.objects.filter(members__pk=user.pk)]

        user_dict["team"] = ", ".join(teams)
        user_dict["service"] = ", ".join(services)
        return user_dict


class CustomFormSubmission(wfm_models.NamedFormSubmission):
    pass


class CustomFormBuilder(
    wfm_models.FileInputFormBuilder,
    wfm_models.StreamFieldFormBuilder,
):
    pass


class CustomSubmissionListView(
    wfm_views.NamedSubmissionsListView,
    wfm_views.FileInputSubmissionsListView,
):
    pass


class FormUploadedFile(models.Model):
    file = models.FileField(upload_to="example_forms/%Y/%m/%d")
    field_name = models.CharField(blank=True, max_length=254)


class AbstractFormPage(
    wfm_models.EmailActionsFormMixin,
    wfm_models.TemplatingFormMixin,
    wfm_models.FileInputFormMixin,
    wfm_models.ConditionalFieldsFormMixin,
    wfm_models.NamedFormMixin,
    wfm_models.StreamFieldFormMixin,
    FormMixin,
    Page,
):
    template_context_class = CustomFormContext
    form_builder = CustomFormBuilder
    file_input_model = FormUploadedFile
    submissions_list_view_class = CustomSubmissionListView

    def get_submission_class(self):
        return CustomFormSubmission

    def serve(self, request, *args, **kwargs):
        is_team_ok = not self.team or Team.objects.filter(members=request.user).exists()
        is_service_ok = not self.service or Service.objects.filter(members=request.user).exists()

        if not is_team_ok or not is_service_ok:
            raise PermissionDenied(_("You are not invited to fill in this form."))

        response = super().serve(request, *args, **kwargs)
        response.context_data["page"].super_title = self.get_parent().form_title
        return response

    class Meta:
        abstract = True


templating_doc = wfm_blocks.DEFAULT_TEMPLATING_DOC
templating_doc["user"]["service"] = _("the form user service (ex: “idea”)")
templating_doc["user"]["team"] = _("the form user team (ex: “gepetto”)")
templating_doc["author"]["service"] = _("the form author service (ex: “idea”)")
templating_doc["author"]["team"] = _("the form author team (ex: “gepetto”)")
templating_doc["form"]["url"] = _("the form url (ex: “https://intranet.laas.fr/form/my-form”)")


class FormFieldsBlock(
    wfm_blocks.FileInputFormBlock,
    wfm_blocks.ConditionalFieldsFormBlock,
    wfm_blocks.TemplatingFormBlock,
    wfm_blocks.StreamFieldFormBlock,
):
    templating_doc = templating_doc

    def get_block_class(self):
        return wfm_blocks.StreamFieldFormBlock


class EmailsToSendBlock(wfm_blocks.TemplatingEmailFormBlock, wfm_blocks.EmailActionsFormBlock):
    templating_doc = templating_doc

    def get_block_class(self):
        return wfm_blocks.EmailActionsFormBlock


class FormPage(AbstractFormPage):
    intro = RichTextField(
        blank=True,
        verbose_name=_("Form introduction text"),
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name=_("Text displayed after form submission"),
    )
    form_fields = StreamField(
        FormFieldsBlock(),
        verbose_name=_("Form fields"),
    )
    emails_to_send = StreamField(
        EmailsToSendBlock(),
        verbose_name=_("E-mails to send after form submission"),
        default=[wfm_blocks.email_to_block(email) for email in DEFAULT_EMAILS],
    )
    team = models.ForeignKey(
        to=Team,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Team"),
    )
    service = models.ForeignKey(
        Service,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Service"),
    )

    content_panels = [
        *AbstractFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
        MultiFieldPanel(
            [
                FieldPanel("team"),
                FieldPanel("service"),
            ],
            _("Scope"),
        ),
        wfm_panels.UniqueResponseFieldPanel(),
    ]
