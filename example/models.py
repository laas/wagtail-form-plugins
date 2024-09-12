from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Page

from wagtail_laas_forms.blocks import FormFieldsBlock, EmailsToSendBlock, Email
from wagtail_laas_forms.models import StreamFieldFormMixin, EmailsFormMixin


DEFAULT_EMAIL_TO_AUTHOR = Email(
    "{author_email}",
    _('New form submission for "{title}"'),
    _('''
Hello,
The form "{title}" received a new submission from user {user} with the following content:

{form_results}

Have a nice day.'''),
).format()

DEFAULT_EMAIL_TO_USER = Email(
    "{user_email}",
    _('Submission confirmation to the form "{title}"'),
    _('''
Hello,
You just sent a new submission to the form "{title}" with the following content:

{form_results}

The form author has been notified.

Have a nice day.'''),
).format()


class LAASFormPage(EmailsFormMixin, StreamFieldFormMixin, Page):
    class Meta:
        abstract = True


class FormPage(LAASFormPage):
    intro = RichTextField(
        blank=True,
        verbose_name=_("Texte d'introduction du formulaire"),
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name=_("Texte affiché après soumission du formulaire"),
    )
    form_fields = StreamField(
        FormFieldsBlock(),
        verbose_name=_("Champs du formulaire"),
    )
    emails_to_send = StreamField(
        EmailsToSendBlock(),
        default=[DEFAULT_EMAIL_TO_AUTHOR, DEFAULT_EMAIL_TO_USER],
        blank=True,
        verbose_name=_("E-mails à envoyer après soumission du formulaire"),
    )

    content_panels = [
        *LAASFormPage.content_panels,
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("emails_to_send"),
    ]
