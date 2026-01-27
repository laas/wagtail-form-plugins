"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
import logging
from typing import cast

from demo.tests.environment import Context

from behave import then, use_step_matcher, when
from bs4 import BeautifulSoup, Tag
from pygments import highlight
from pygments.formatters import TerminalFormatter  # ty: ignore unresolved-import
from pygments.lexers import HtmlLexer  # ty: ignore unresolved-import

use_step_matcher("re")

logger = logging.getLogger(__name__)


@when(r'I visit "(?P<url>.+?)"')
def visit(context: Context, url: str):
    context.response = context.test.client.get(url, follow=True)
    context.test.assertEqual(context.response.status_code, 200)
    context.soup = BeautifulSoup(context.response.text, "html.parser")

    context.form_data = {}
    if context.soup.form is not None:
        for field in context.soup.form.find_all(["input", "select", "textarea"]):
            field_name = field.get("name")
            context.test.assertIsNotNone(field_name, "field name not found")
            field_value = field.checked if field.type == "checkbox" else field.get("value")
            context.form_data[field_name] = field_value


@when(r'I fill the "(?P<input_name>.+?)" input with "(?P<input_value>.+?)"')
def fill_form(context: Context, input_name: str, input_value: str):
    context.form_data[input_name] = input_value


@when("I validate the form")
def validate_form(context: Context):
    context.test.assertNotEqual(len(context.form_data.keys()), 0, "no form data")
    context.test.assertIsNotNone(context.soup.form, "form not found")
    form_action = str(cast("Tag", context.soup.form).get("action", ""))
    context.response = context.test.client.post(form_action, context.form_data, follow=True)
    context.test.assertEqual(context.response.status_code, 200)
    context.soup = BeautifulSoup(context.response.text, "html.parser")


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
