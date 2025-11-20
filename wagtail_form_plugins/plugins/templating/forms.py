"""Form-related classes for the Templating plugin."""

from wagtail_form_plugins.streamfield.forms import StreamFieldFormBuilder


class TemplatingFormBuilder(StreamFieldFormBuilder):
    """Form builder mixin that use streamfields to define form fields in form admin page."""
