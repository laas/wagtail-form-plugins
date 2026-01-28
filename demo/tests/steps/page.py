"""Common step definitions to handle web page related checks."""

# ruff: noqa: D103, ANN201, PT009
import logging
from urllib.parse import urlparse

from demo.tests.environment import Context

from behave import then, use_step_matcher, when
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import TerminalFormatter  # ty: ignore unresolved-import
from pygments.lexers import HtmlLexer  # ty: ignore unresolved-import

use_step_matcher("re")
BASE_URL = "http://localhost:8000"
LOGGER = logging.getLogger(__name__)


@when(r'I visit "(?P<url>.+?)"')
def visit(context: Context, url: str):
    context.response = context.test.client.get(f"{BASE_URL}{url}", follow=True)
    context.soup = BeautifulSoup(context.response.text, "html.parser")
    context.test.assertEqual(context.response.status_code, 200)

    context.form_data = {}
    if context.soup.form is not None:
        for field in context.soup.form.find_all(["input", "select", "textarea"]):
            field_name = field.get("name")
            context.test.assertIsNotNone(field_name, "field name not found")
            field_value = field.checked if field.type == "checkbox" else field.get("value")
            context.form_data[field_name] = field_value


@when("I click on (?:the|that) link")
def use_link(context: Context):
    context.test.assertTrue(hasattr(context, "link"), "no link found in previous steps")

    url = urlparse(context.link)
    url_path = url.path + (f"?{url.query}" if url.query else "")
    visit(context, url_path)


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


@then(r"I should see (?:a|an|the) (?P<message_tag>[\w-]* )(?P<message_level>\w+) message")
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
    LOGGER.info(highlight(html_content, HtmlLexer(), TerminalFormatter()))
