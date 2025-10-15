from .blocks import StreamFieldFormBlock
from .forms import StreamFieldFormBuilder, StreamFieldFormField
from .models import StreamFieldFormPage, StreamFieldFormSubmission
from .views import StreamFieldSubmissionsListView


class Plugin:
    form_block_class = StreamFieldFormBlock
    form_builder_class = StreamFieldFormBuilder
    form_field_class = StreamFieldFormField
    form_submission_class = StreamFieldFormSubmission
    form_page_class = StreamFieldFormPage
    submission_list_view_class = StreamFieldSubmissionsListView


class WagtailFormPlugin:
    def __init__(self, *plugins: type[Plugin]) -> None:
        self.plugins = plugins

    @property
    def form_block_classes(self) -> list[type[StreamFieldFormBlock]]:
        base_classes = [
            plugin.form_block_class
            for plugin in self.plugins
            if plugin.form_block_class != StreamFieldFormBlock
        ]
        return base_classes if base_classes else [StreamFieldFormBlock]

    @property
    def form_builder_classes(self) -> list[type[StreamFieldFormBuilder]]:
        base_classes = [
            plugin.form_builder_class
            for plugin in self.plugins
            if plugin.form_builder_class != StreamFieldFormBuilder
        ]
        return base_classes if base_classes else [StreamFieldFormBuilder]

    @property
    def form_field_classes(self) -> list[type[StreamFieldFormField]]:
        base_classes = [
            plugin.form_field_class
            for plugin in self.plugins
            if plugin.form_field_class != StreamFieldFormField
        ]
        return base_classes if base_classes else [StreamFieldFormField]

    @property
    def form_submission_classes(self) -> list[type[StreamFieldFormSubmission]]:
        base_classes = [
            plugin.form_submission_class
            for plugin in self.plugins
            if plugin.form_submission_class != StreamFieldFormSubmission
        ]
        return base_classes if base_classes else [StreamFieldFormSubmission]

    @property
    def form_page_classes(self) -> list[type[StreamFieldFormPage]]:
        base_classes = [
            plugin.form_page_class
            for plugin in self.plugins
            if plugin.form_page_class != StreamFieldFormPage
        ]
        return base_classes if base_classes else [StreamFieldFormPage]

    @property
    def submission_list_view_classes(self) -> list[type[StreamFieldSubmissionsListView]]:
        base_classes = [
            plugin.submission_list_view_class
            for plugin in self.plugins
            if plugin.submission_list_view_class != StreamFieldSubmissionsListView
        ]
        return base_classes if base_classes else [StreamFieldSubmissionsListView]
