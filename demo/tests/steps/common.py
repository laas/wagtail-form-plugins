"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009

from demo.tests.environment import Context

from behave import then, when
from bs4 import BeautifulSoup


@when("I visit '{url}'")
def visit(context: Context, url: str):
    context.response = context.test.client.get(url, follow=True)
    context.soup = BeautifulSoup(context.response.text, "html.parser")
    context.test.assertEqual(context.response.status_code, 200)


@then("the page title should be '{page_title}'")
def check_page_title(context: Context, page_title: str):
    context.test.assertEqual(context.soup.title.string.strip(), page_title)  # ty: ignore possibly-missing-attribute


@then("I should see the title '{html_title}'")
def check_html_title(context: Context, html_title: str):
    titles = [title.string.strip() for title in context.soup.find_all("h1")]  # ty: ignore possibly-missing-attribute
    context.test.assertIn(html_title, titles)


@then("I should see '{text}'")
def check_any(context: Context, text: str):
    context.test.assertIn(text, context.response.text)


@then("I should see a {type} input named '{name}'")
def check_field(context: Context, input_type: str, name: str):
    input_attrs = {"type": input_type, "name": name}
    soup_input = context.soup.find("input", attrs=input_attrs)
    context.test.assertIsNotNone(soup_input)


@then("I should see {amount} inputs in total")
def check_fields_amount(context: Context, amount: int):
    soup_inputs = [
        f"{si.attrs.get('type', '-')} {si.attrs.get('name', '-')}"
        for si in context.soup.find_all("input")
    ]
    context.test.assertEqual(len(soup_inputs), amount, ", ".join(soup_inputs))
