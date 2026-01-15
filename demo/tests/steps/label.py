"""Steps definition for the Label plugin."""

# ruff: noqa: D103, ANN201, T201

from behave import given, then, when
from behave.runner import Context


@given("that an empty form named '{form_title}' exists")
def add_form(_context: Context, form_title: str):
    print(f"creating a form named {form_title}...")


@given("I add a {field_type} field as follow:")
def add_label(_context: Context, field_type: str):
    print(f"creating a {field_type} field...")


@when("I visit the form named '{form_title}'")
def visit_form(_context: Context, form_title: str):
    print(f"visiting the form '{form_title}'...")


@then("I should see the following elements:")
def see_elements(_context: Context):
    print("looking for precense elements in page...")


@then("I should not see any form subtitle help")
@then("I should not see any form subtitle or subtitle help")
def dont_see(_context: Context):
    print("looking for absence elements in page...")
