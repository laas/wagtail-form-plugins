"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
import logging

from demo.tests.environment import Context

from behave import then, use_step_matcher

use_step_matcher("re")

logger = logging.getLogger(__name__)


@then(r'I should see (?:a|an) (?P<input_type>\w+) input named "(?P<input_name>.+?)"')
def check_form_field(context: Context, input_type: str, input_name: str):
    soup_input = context.soup.find("input", {"type": input_type, "name": input_name})
    context.test.assertIsNotNone(soup_input)


@then(r"I should see (?P<amount>\d+) inputs? in total")
def check_form_fields_amount(context: Context, amount: str):
    soup_inputs = [
        f"{si.attrs.get('type', '-')} {si.attrs.get('name', '-')}"
        for si in context.soup.find_all("input")
        if si.get("type", "-") != "hidden"
    ]
    context.test.assertEqual(len(soup_inputs), int(amount), ", ".join(soup_inputs))
