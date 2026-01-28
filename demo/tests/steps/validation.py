"""Steps used for the TokenValidation plugin."""

# ruff: noqa: D103, ANN201
from demo.tests.environment import Context
from demo.tests.steps import email as step_email
from demo.tests.steps.page import use_link

from behave import then, when


@when("I click on the validation link")
def use_validation_link(context: Context):
    use_link(context)


@then(r"I should receive a validation email from (?P<sender>\S+@\S+) to (?P<recipient>\S+@\S+)")
def check_validation_email(context: Context, sender: str, recipient: str):
    step_email.check_email(context)
    step_email.check_email_subject(context, "validation")
    step_email.check_email_from(context, sender)
    step_email.check_email_to(context, recipient)
    step_email.check_link_in_email_body(context)
