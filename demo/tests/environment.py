"""Functions used to customize Behave."""

from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase

from behave.model import Scenario
from behave.runner import Context as RunnerContext
from bs4 import BeautifulSoup


class Context(RunnerContext):
    """Only used for better typing."""

    test: TestCase
    soup: BeautifulSoup
    last_email: EmailMultiAlternatives
    link: str


def before_scenario(_context: Context, _scenario: Scenario) -> None:
    """Empty email box before running each Behave scenario."""
    mail.outbox = []
