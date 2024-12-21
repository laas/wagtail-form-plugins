from wagtail.admin.panels import FieldPanel


class UniqueResponseFieldPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        kwargs["field_name"] = "unique_response"
        super().__init__(*args, **kwargs)
