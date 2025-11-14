"""Panel classes of the TokenValidation plugin."""

from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class ValidationFieldPanel(MultiFieldPanel):
    """A panel used to add token validation field to the form admin page."""

    def __init__(self, *args, **kwargs):
        kwargs["children"] = [
            FieldPanel("validation_title"),
            FieldPanel("validation_body"),
        ]
        kwargs["heading"] = "Validation e-mail"
        super().__init__(*args, **kwargs)
