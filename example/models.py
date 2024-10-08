from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Page

from wagtail_form_mixins.conditional_fields.blocks import ConditionalFieldsFormBlock
from wagtail_form_mixins.conditional_fields.models import ConditionalFieldsFormMixin
from wagtail_form_mixins.streamfield.models import StreamFieldFormMixin
from wagtail_form_mixins.streamfield.blocks import StreamFieldFormBlock
from wagtail_form_mixins.actions.models import EmailActionsFormMixin
from wagtail_form_mixins.actions.blocks import EmailActionsFormBlock, email_to_block
from wagtail_form_mixins.templating.models import TemplatingFormMixin
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
    }
]


class AbstractFormPage(
    EmailActionsFormMixin,
    TemplatingFormMixin,
    ConditionalFieldsFormMixin,
    StreamFieldFormMixin,
    Page,
):
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
        verbose_name = _("E-mails to send after form submission"),
        default=[email_to_block(email) for email in DEFAULT_EMAILS]
    )

    content_panels = [
        *AbstractFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
    ]
