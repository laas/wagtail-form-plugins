"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
from urllib.parse import urlparse

from demo.tests.environment import Context

from behave import use_step_matcher, when
from bs4 import BeautifulSoup

use_step_matcher("re")


@when(r'I visit "(?P<url>.+?)"')
def visit(context: Context, url: str):
    context.response = context.test.client.get(url, follow=True)
    context.soup = BeautifulSoup(context.response.text, "html.parser")
    context.test.assertEqual(context.response.status_code, 200)

    context.form_data = {}
    if context.soup.form is not None:
        for field in context.soup.form.find_all(["input", "select", "textarea"]):
            field_name = field.get("name")
            context.test.assertIsNotNone(field_name, "field name not found")
            field_value = field.checked if field.type == "checkbox" else field.get("value")
            context.form_data[field_name] = field_value


@when("I click on that link")
def use_link(context: Context):
    context.test.assertTrue(hasattr(context, "link"), "no link found in previous steps")

    url = urlparse(context.link)
    url_path = url.path + (f"?{url.query}" if url.query else "")
    visit(context, url_path)
