from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from wagtail_form_mixins.conditional_fields.blocks import ConditionalFieldsFormBlock
from wagtail_form_mixins.conditional_fields.models import ConditionalFieldsFormMixin
from wagtail_form_mixins.streamfield.models import StreamFieldFormMixin
from wagtail_form_mixins.streamfield.blocks import StreamFieldFormBlock
from wagtail_form_mixins.actions.models import EmailActionsFormMixin
from wagtail_form_mixins.actions.blocks import EmailActionsFormBlock, email_to_block
from wagtail_form_mixins.templating.models import TemplatingFormMixin, FormContext
from wagtail_form_mixins.templating.blocks import TemplatingFormBlock, TemplatingEmailFormBlock


DEFAULT_EMAILS = [
    {
        "recipient_list": "{author.email}",
        "subject": 'Nouvelle entrée pour le formulaire "{form.title}"',
        "message": """Bonjour {author.full_name},
Le {result.publish_date} à {result.publish_time}, l’utilisateur {user.full_name} a complété le formulaire "{form.title}", avec le contenu suivant:

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


class MyFormContext(FormContext):
    def format_user(self, user: User):
        user_dict = super().format_user(user)

        teams = [service.name for service in Team.objects.filter(members__pk=user.pk)]
        services = [service.name for service in Service.objects.filter(members__pk=user.pk)]

        user_dict["team"] = ", ".join(teams)
        user_dict["service"] = ", ".join(services)
        return user_dict


class AbstractFormPage(
    EmailActionsFormMixin,
    TemplatingFormMixin,
    ConditionalFieldsFormMixin,
    StreamFieldFormMixin,
    Page,
):
    template_context_class = MyFormContext

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        response.context_data["page"].super_title = self.get_parent().form_title
        return response

    class Meta:
        abstract = True


class FormFieldsBlock(ConditionalFieldsFormBlock, TemplatingFormBlock, StreamFieldFormBlock):
    def get_block_class(self):
        return StreamFieldFormBlock


class EmailsToSendBlock(TemplatingEmailFormBlock, EmailActionsFormBlock):
    def get_block_class(self):
        return EmailActionsFormBlock


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
        default=[email_to_block(email) for email in DEFAULT_EMAILS],
    )

    content_panels = [
        *AbstractFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
    ]
