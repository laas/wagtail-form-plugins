from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from wagtail_laas_forms.blocks import FormFieldsBlock
from wagtail_laas_forms.models import AbstractEmailStreamFieldForm


class FormPage(AbstractEmailStreamFieldForm):
    intro = RichTextField(blank=True)
    form_fields = StreamField(FormFieldsBlock())
    thank_you_text = RichTextField(blank=True)

    content_panels = [
        *AbstractEmailStreamFieldForm.content_panels,
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        FieldPanel('form_fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
