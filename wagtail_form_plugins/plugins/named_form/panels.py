"""Panel classes of the Named Form plugin."""

from wagtail.admin.panels import FieldPanel


class UniqueResponseFieldPanel(FieldPanel):
    """A panel used to add unique response field to the form admin page."""

    def __init__(self, *args, **kwargs):
        kwargs["field_name"] = "unique_response"
        super().__init__(*args, **kwargs)
