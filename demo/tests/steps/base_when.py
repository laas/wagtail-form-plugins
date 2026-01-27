"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
import logging
from typing import cast

from demo.tests.environment import Context

from behave import use_step_matcher, when
from bs4 import BeautifulSoup, Tag

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
