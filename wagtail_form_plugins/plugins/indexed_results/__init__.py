"""Indexed results plugin: add an index value in the results."""

from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import IndexedResultsFormPage, IndexedResultsFormSubmission


class IndexedResults(Plugin):
    """Indexed results plugin: add an index value in the results."""

    form_page_class = IndexedResultsFormPage
    form_submission_class = IndexedResultsFormSubmission


__all__ = [
    "IndexedResultsFormPage",
    "IndexedResultsFormSubmission",
]
