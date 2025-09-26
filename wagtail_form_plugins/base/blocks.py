"""Base classes for block mixins."""

from typing import ClassVar

from wagtail import blocks


class BaseFormFieldsBlock(blocks.StreamBlock):
    """Base class for block mixins."""

    subclasses: ClassVar = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_blocks(self) -> dict[str, blocks.StreamBlock]:
        """Get all the declared blocks from all subclasses."""
        declared_blocks = {}
        for subclass in self.subclasses:
            declared_blocks.update(subclass.declared_blocks)
        return declared_blocks
