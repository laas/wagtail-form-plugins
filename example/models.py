from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Page

from wagtail_form_mixins.conditions.blocks import RulesBlockMixin
from wagtail_form_mixins.conditions.models import ConditionalFieldsMixin
from wagtail_form_mixins.streamfield.models import StreamFieldFormMixin
from wagtail_form_mixins.streamfield.blocks import FormFieldsBlock
from wagtail_form_mixins.emails.models import EmailsFormMixin
from wagtail_form_mixins.emails.blocks import Email, EmailsToSendBlock


DEFAULT_EMAIL_TO_AUTHOR = Email(
    recipient_list="{author_email}",
    subject='Nouvelle entrée pour le formulaire "{title}"',
    message='''
Bonjour,
Le formulaire "{title}" vient d'être complété par l'utilisateur {user}, avec le contenu suivant:
{form_results}
Bonne journée.''',
).format()

DEFAULT_EMAIL_TO_USER = Email(
    recipient_list="{user_email}",
    subject='Submission confirmation to the form "{title}"',
    message='''
Bonjour,
Vous venez de compléter le formulaire "{title}", avec le contenu suivant:
{form_results}
L'auteur du formulaire en a été informé.
Bonne journée.''',
).format()


class LAASFormPage(EmailsFormMixin, ConditionalFieldsMixin, StreamFieldFormMixin, Page):
    class Meta:
        abstract = True


class ConditionalFormFieldsBlock(RulesBlockMixin, FormFieldsBlock):
    def get_block_class(self):
        return FormFieldsBlock


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
        ConditionalFormFieldsBlock(),
        verbose_name="Champs du formulaire",
    )
    emails_to_send = StreamField(
        EmailsToSendBlock(),
        default=[DEFAULT_EMAIL_TO_AUTHOR, DEFAULT_EMAIL_TO_USER],
        blank=True,
        verbose_name="E-mails à envoyer après soumission du formulaire",
    )

    content_panels = [
        *LAASFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
    ]
