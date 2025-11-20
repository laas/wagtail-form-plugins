"""Handles the plugins logic."""

from django.templatetags.static import static
from django.utils.html import format_html

from .blocks import StreamFieldFormBlock
from .forms import StreamFieldFormBuilder, StreamFieldFormField
from .models import StreamFieldFormPage, StreamFieldFormSubmission
from .views import StreamFieldSubmissionsListView


class Plugin:
    """Hight-level representation of a plugin, defining the classes used in it."""

    form_block_class = StreamFieldFormBlock
    form_builder_class = StreamFieldFormBuilder
    form_field_class = StreamFieldFormField
    form_submission_class = StreamFieldFormSubmission
    form_page_class = StreamFieldFormPage
    submission_list_view_class = StreamFieldSubmissionsListView

    @classmethod
    def get_injected_admin_css(cls) -> str:
        """Return the css to inject in the form admin page."""
        return ""


class WagtailFormPlugin:
    """Utility class used to define the plugins to use and get the classes used by them."""

    def __init__(self, *plugins: type[Plugin]) -> None:
        self.plugins = plugins

    @property
    def form_block_classes(self) -> list[type[StreamFieldFormBlock]]:
        """Return the StreamFieldFormBlock classes used by the plugins."""
        base_classes = [
            plugin.form_block_class
            for plugin in self.plugins
            if plugin.form_block_class != StreamFieldFormBlock
        ]
        return base_classes if base_classes else [StreamFieldFormBlock]

    @property
    def form_builder_classes(self) -> list[type[StreamFieldFormBuilder]]:
        """Return the StreamFieldFormBuilder classes used by the plugins."""
        base_classes = [
            plugin.form_builder_class
            for plugin in self.plugins
            if plugin.form_builder_class != StreamFieldFormBuilder
        ]
        return base_classes if base_classes else [StreamFieldFormBuilder]

    @property
    def form_field_classes(self) -> list[type[StreamFieldFormField]]:
        """Return the StreamFieldFormField classes used by the plugins."""
        base_classes = [
            plugin.form_field_class
            for plugin in self.plugins
            if plugin.form_field_class != StreamFieldFormField
        ]
        return base_classes if base_classes else [StreamFieldFormField]

    @property
    def form_submission_classes(self) -> list[type[StreamFieldFormSubmission]]:
        """Return the StreamFieldFormSubmission classes used by the plugins."""
        base_classes = [
            plugin.form_submission_class
            for plugin in self.plugins
            if plugin.form_submission_class != StreamFieldFormSubmission
        ]
        return base_classes if base_classes else [StreamFieldFormSubmission]

    @property
    def form_page_classes(self) -> list[type[StreamFieldFormPage]]:
        """Return the StreamFieldFormPage classes used by the plugins."""
        base_classes = [
            plugin.form_page_class
            for plugin in self.plugins
            if plugin.form_page_class != StreamFieldFormPage
        ]
        return base_classes if base_classes else [StreamFieldFormPage]

    @property
    def submission_list_view_classes(self) -> list[type[StreamFieldSubmissionsListView]]:
        """Return the StreamFieldSubmissionsListView classes used by the plugins."""
        base_classes = [
            plugin.submission_list_view_class
            for plugin in self.plugins
            if plugin.submission_list_view_class != StreamFieldSubmissionsListView
        ]
        return base_classes if base_classes else [StreamFieldSubmissionsListView]

    def injected_admin_css(self) -> str:
        """Return a string containing the injected css of the plugins."""
        streamfield_injected_admin_css = format_html(
            '<link rel="stylesheet" href="{href}">',
            href=static("wagtail_form_plugins/streamfield/css/form_admin.css"),
        )
        all_injected_admin_css = [
            streamfield_injected_admin_css,
            *[plugin.get_injected_admin_css() for plugin in self.plugins],
        ]
        return "\n".join(all_injected_admin_css)
