"""Steps used for the TokenValidation plugin."""

# ruff: noqa: D103, ANN201
from demo.tests.environment import Context
from demo.tests.steps import email as step_email
from demo.tests.steps import form as step_form
from demo.tests.steps import page as step_page

from behave import then, when


@when("I click on the validation link")
def use_validation_link(context: Context):
    step_page.use_link(context)


@then(r'I should see the form validation page of "(?P<form_title>.+?)"')
def check_form_validation_page(context: Context, form_title: str):
    step_form.check_form_page(context, form_title)
    step_form.check_form_field(context, "email", "validation_email")
    step_form.check_form_fields_amount(context, 1)


@then(r"I should receive at (?P<recipient>\S+@\S+) a validation email from (?P<sender>\S+@\S+)")
def check_validation_email(context: Context, sender: str, recipient: str):
    step_email.check_email(context)
    step_email.check_email_subject(context, "validation")
    step_email.check_email_from(context, sender)
    step_email.check_email_to(context, recipient)
    step_email.check_link_in_email_body(context)
