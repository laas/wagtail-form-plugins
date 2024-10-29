from wagtail import blocks


class FormFieldsBlockMixin(blocks.StreamBlock):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_blocks(self):
        declared_blocks = {}
        for subclass in self.subclasses:
            declared_blocks.update(subclass.declared_blocks)
        return declared_blocks
