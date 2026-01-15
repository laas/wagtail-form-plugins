"""Functions used to customize Behave."""

from django.test import TestCase

from behave.runner import Context as RunnerContext
from bs4 import BeautifulSoup


class Context(RunnerContext):
    """Only used for better typing."""

    test: TestCase
    soup: BeautifulSoup
