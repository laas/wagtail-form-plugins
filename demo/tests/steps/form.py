"""Step definitions related to forms checks."""

# ruff: noqa: D103, ANN201, PT009
from typing import cast

from wagtail.models import Page

from demo.models import FormIndexPage, FormPage
from demo.tests.environment import Context
from demo.tests.steps.page import check_page_title, check_template_name

from behave import given, then, use_step_matcher, when
from bs4 import BeautifulSoup, Tag

use_step_matcher("re")


@given(r"the form index page exists")
def create_form_index_page(context: Context):
    Page.objects.exclude(slug="root").exclude(slug="home").delete()
    FormIndexPage.create_if_missing(Page.objects.get(slug="home"))
    context.test.assertTrue(FormIndexPage.objects.exists())


@given(r'a form named "(?P<form_title>.+?)" exists')
def create_form_page(context: Context, form_title: str):
    create_form_index_page(context)

    form_index_page = FormIndexPage.objects.first()
    if not form_index_page:
        context.test.fail("FormIndexPage not created")
        return

    form_page = FormPage(title=form_title)
    form_index_page.add_child(instance=form_page)

    revision = form_page.save_revision()
    revision.publish()

    context.test.assertTrue(FormPage.objects.filter(title=form_title).exists())


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


@then(r'I should see the form page "(?P<form_title>.+?)"')
def use_link(context: Context, form_title: str):
    check_template_name(context, "demo/form_page.html")
    check_page_title(context, form_title)
    check_form_field(context, "email", "validation_email")
    check_form_fields_amount(context, 1)


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
