from .blocks import StreamFieldFormBlock
from .forms import StreamFieldFormBuilder, StreamFieldFormField
from .models import StreamFieldFormPage, StreamFieldFormSubmission
from .views import StreamFieldSubmissionsListView


class DefaultFormBlock(StreamFieldFormBlock):
    class Meta:  # type: ignore
        abstract = True


class DefaultFormBuilder(StreamFieldFormBuilder):
    class Meta:  # type: ignore
        abstract = True


class DefaultFormField(StreamFieldFormField):
    class Meta:  # type: ignore
        abstract = True


class DefaultFormSubmission(StreamFieldFormSubmission):
    class Meta:  # type: ignore
        abstract = True


class DefaultFormPage(StreamFieldFormPage):
    class Meta:  # type: ignore
        abstract = True


class DefaultSubmissionsListView(StreamFieldSubmissionsListView):
    class Meta:  # type: ignore
        abstract = True


class Plugin:
    form_block_class = DefaultFormBlock
    form_builder_class = DefaultFormBuilder
    form_field_class = DefaultFormField
    form_submission_class = DefaultFormSubmission
    form_page_class = DefaultFormPage
    submission_list_view_class = DefaultSubmissionsListView


class WagtailFormPlugin:
    def __init__(self, *plugins: type[Plugin]) -> None:
        self.plugins = plugins

    @property
    def form_block_classes(self) -> set[type[StreamFieldFormBlock]]:
        return {plugin.form_block_class for plugin in self.plugins}

    @property
    def form_builder_classes(self) -> set[type[StreamFieldFormBuilder]]:
        return {plugin.form_builder_class for plugin in self.plugins}

    @property
    def form_field_classes(self) -> set[type[StreamFieldFormField]]:
        return {plugin.form_field_class for plugin in self.plugins}

    @property
    def form_submission_classes(self) -> set[type[StreamFieldFormSubmission]]:
        return {plugin.form_submission_class for plugin in self.plugins}

    @property
    def form_page_classes(self) -> set[type[StreamFieldFormPage]]:
        return {plugin.form_page_class for plugin in self.plugins}

    @property
    def submission_list_view_classes(self) -> set[type[StreamFieldSubmissionsListView]]:
        return {plugin.submission_list_view_class for plugin in self.plugins}
