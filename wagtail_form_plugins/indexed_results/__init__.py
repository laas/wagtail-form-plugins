from wagtail_form_plugins.streamfield.plugin import Plugin

from .models import IndexedResultsFormPage, IndexedResultsFormSubmission


class IndexedResults(Plugin):
    form_page_class = IndexedResultsFormPage
    form_submission_class = IndexedResultsFormSubmission


__all__ = [
    "IndexedResultsFormPage",
    "IndexedResultsFormSubmission",
]
