"""Steps used for email validation."""

# ruff: noqa: D103, ANN201
from demo.tests.environment import Context
from demo.tests.steps import email_then
from demo.tests.steps.base_when import use_link

from behave import then, when


@when("I click on the validation link")
def use_validation_link(context: Context):
    use_link(context)


@then(r"I should receive a validation email from (?P<sender>\S+@\S+) to (?P<recipient>\S+@\S+)")
def check_validation_email(context: Context, sender: str, recipient: str):
    email_then.check_email(context)
    email_then.check_email_subject(context, "validation")
    email_then.check_email_from(context, sender)
    email_then.check_email_to(context, recipient)
    email_then.check_link_in_email_body(context)
