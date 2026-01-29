"""Step definitions related to forms checks."""

# ruff: noqa: D103, ANN201, PT009, E501
from typing import cast

from wagtail.models import Page

from demo.models import CustomUser, FormIndexPage, FormPage
from demo.tests.environment import Context
from demo.tests.steps import email as step_email
from demo.tests.steps import page as step_page

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
    form_index_page = cast("FormIndexPage", FormIndexPage.objects.first())
    context.test.assertIsNotNone(form_index_page)

    form_page = FormPage(title=form_title, depth=form_index_page.depth + 1)
    form_index_page.add_child(instance=form_page)
    form_page.save_revision().publish()

    context.test.assertTrue(FormPage.objects.filter(title=form_title).exists())


@given(r'the form "(?P<form_title>.+?)" is created by the user (?P<username>\w+) \((?P<email>\S+@\S+)\)')  # fmt: skip
def set_form_owner(context: Context, form_title: str, username: str, email: str):
    form_page = FormPage.objects.get(title=form_title)
    form_page.owner = CustomUser.objects.create_user(username, email, "password")
    form_page.save()
    context.test.assertEqual(form_page.owner.username, username)
    context.test.assertEqual(form_page.owner.email, email)


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


@then("I should see the form index page")
def check_form_index_page(context: Context):
    step_page.check_template_name(context, "demo/form_index_page.html")
    step_page.check_page_title(context, "Forms")


@then(r'I should see the form page "(?P<form_title>.+?)"')
def check_form_page(context: Context, form_title: str):
    step_page.check_template_name(context, "demo/form_page.html")
    step_page.check_page_title(context, form_title)
    step_page.check_html_title(context, form_title, "h2")


@then(r'I should see the form landing page "(?P<form_title>.+?)"')
def check_form_landing_page(context: Context, form_title: str):
    step_page.check_template_name(context, "demo/form_page_landing.html")
    step_page.check_page_title(context, form_title)
    step_page.check_html_title(context, form_title, "h2")


@then(r'I should see (?:a|an) (?P<input_type>\w+) input named "(?P<input_name>.+?)"')
def check_form_field(context: Context, input_type: str, input_name: str):
    soup_input = context.soup.find("input", {"type": input_type, "name": input_name})
    context.test.assertIsNotNone(soup_input)


@then(r"I should see (?P<amount>\d+) form fields?")
def check_form_fields_amount(context: Context, amount: str):
    soup_inputs = [
        f"{si.attrs.get('type', '-')} {si.attrs.get('name', '-')}"
        for si in context.soup.find_all("input")
        if si.get("type", "-") != "hidden"
    ]
    context.test.assertEqual(len(soup_inputs), int(amount), ", ".join(soup_inputs))


@then(r'I should receive at (?P<recipient>\S+@\S+) a confirmation email from (?P<sender>\S+@\S+) about the form "(?P<form_title>.+?)"')  # fmt: skip
def check_validation_email(context: Context, sender: str, recipient: str, form_title: str):
    step_email.check_email(context)
    step_email.check_email_subject(context, f'submission of the form "{form_title}"')
    step_email.check_email_from(context, sender)
    step_email.check_email_to(context, recipient)
    step_email.check_email_text_body(context, f'you just submitted the form "{form_title}"')
    step_email.check_email_html_body(context, f'you just submitted the form "{form_title}"')


@then(r'the form admin \((?P<recipient>\S+@\S+)\) should receive an information email from (?P<sender>\S+@\S+) about the form "(?P<form_title>.+?)"')  # fmt: skip
def check_information_email(context: Context, sender: str, recipient: str, form_title: str):
    step_email.check_email(context)
    step_email.check_email_subject(context, f'New entry for form "{form_title}"')
    step_email.check_email_from(context, sender)
    step_email.check_email_to(context, recipient)
    step_email.check_email_text_body(context, f'has submitted the form "{form_title}"')
    step_email.check_email_html_body(context, f'has submitted the form "{form_title}"')
