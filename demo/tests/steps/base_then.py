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


@then(r'I should see the title "(?P<html_title>.+?)"')
def check_html_title(context: Context, html_title: str):
    titles = [title.string.strip() for title in context.soup.find_all("h1")]  # ty: ignore possibly-missing-attribute
    context.test.assertIn(html_title, titles)


@then(r"I should see (?:a|an) (?P<message_tag>\w* )(?P<message_level>\w+) message")
def check_message(context: Context, message_tag: str, message_level: str):
    message_classes = [f"alert-{message_level}", message_tag]
    logger.info(message_classes)
    logger.info("\n")
    soup_message = context.soup.find("div", {"class": message_classes})
    context.test.assertIsNotNone(soup_message, f"{message_classes} not found")


@then(r'I should see (?:a|an) (?P<input_type>\w+) input named "(?P<input_name>.+?)"')
def check_field(context: Context, input_type: str, input_name: str):
    soup_input = context.soup.find("input", {"type": input_type, "name": input_name})
    context.test.assertIsNotNone(soup_input)


@then(r"I should see (?P<amount>\d+) inputs? in total")
def check_fields_amount(context: Context, amount: int):
    soup_inputs = [
        f"{si.attrs.get('type', '-')} {si.attrs.get('name', '-')}"
        for si in context.soup.find_all("input")
        if si.get("type", "-") != "hidden"
    ]
    context.test.assertEqual(len(soup_inputs), int(amount), ", ".join(soup_inputs))


@then(r"dump the page content")
def dump_html(context: Context):
    html_content = context.soup.prettify()
    colored_html = highlight(html_content, HtmlLexer(), TerminalFormatter())
    logger.info(colored_html)


@then(r'the template used should be "(?P<input_name>.+?)"')
def check_template(context: Context, input_name: str):
    context.test.assertEqual(context.response.template_name, input_name)
