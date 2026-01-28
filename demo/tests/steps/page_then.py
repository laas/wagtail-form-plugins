"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
import logging

from demo.tests.environment import Context

from behave import then, use_step_matcher
from pygments import highlight
from pygments.formatters import TerminalFormatter  # ty: ignore unresolved-import
from pygments.lexers import HtmlLexer  # ty: ignore unresolved-import

use_step_matcher("re")

logger = logging.getLogger(__name__)


@then(r'the page title should be "(?P<page_title>.+?)"')
def check_page_title(context: Context, page_title: str):
    context.test.assertEqual(context.soup.title.string.strip(), page_title)  # ty: ignore possibly-missing-attribute


@then(r"the page should contain a (?P<div_id>[\w-]*) element")
def check_div(context: Context, div_id: str):
    context.test.assertIsNotNone(context.soup.find("div", {"id": div_id}))


@then(r'I should see the title "(?P<html_title>.+?)"')
def check_html_title(context: Context, html_title: str):
    titles = [title.string.strip() for title in context.soup.find_all("h1")]  # ty: ignore possibly-missing-attribute
    context.test.assertIn(html_title, titles)


@then(r"I should see (?:a|an) (?P<message_tag>[\w-]* )(?P<message_level>\w+) message")
def check_django_message(context: Context, message_tag: str, message_level: str):
    message_classes = [f"alert-{message_level}", message_tag]
    soup_message = context.soup.find("div", {"class": message_classes})
    context.test.assertIsNotNone(soup_message, f"classes {', '.join(message_classes)} not found")


@then(r'the template used should be "(?P<input_name>.+?)"')
def check_template_name(context: Context, input_name: str):
    context.test.assertEqual(context.response.template_name, input_name)


@then(r"I dump the page content")
def dump_html(context: Context):
    html_content = context.soup.prettify()
    logger.info(highlight(html_content, HtmlLexer(), TerminalFormatter()))
