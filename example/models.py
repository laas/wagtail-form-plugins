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


DEFAULT_EMAILS = [
    {
        "recipient_list": "{author_email}",
        "subject": 'Nouvelle entrée pour le formulaire "{title}"',
        "message": '''Bonjour,
Le formulaire "{title}" vient d'être complété par l’utilisateur {user}, avec le contenu suivant:
{form_results}
Bonne journée.''',
    },
    {
        "recipient_list": "{user_email}",
        "subject": 'Confirmation de l’envoi du formulaire "{title}"',
        "message": '''Bonjour,
Vous venez de compléter le formulaire "{title}", avec le contenu suivant:
{form_results}
L’auteur du formulaire en a été informé.
Bonne journée.''',
    }
]

class LAASFormPage(TemplatingFormMixin, EmailActionsFormMixin, ConditionalFieldsFormMixin, StreamFieldFormMixin, Page):
    class Meta:
        abstract = True


class StreamFieldConditionsFormBlock(ConditionalFieldsFormBlock, StreamFieldFormBlock):
    def get_block_class(self):
        return StreamFieldFormBlock


class FormPage(LAASFormPage):
    intro = RichTextField(
        blank=True,
        verbose_name="Texte d'introduction du formulaire",
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name="Texte affiché après soumission du formulaire",
    )
    form_fields = StreamField(
        StreamFieldConditionsFormBlock(),
        verbose_name="Champs du formulaire",
    )
    emails_to_send = StreamField(
        EmailActionsFormBlock(),
        default=[email_to_block(email) for email in DEFAULT_EMAILS]
    )

    content_panels = [
        *LAASFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
    ]
