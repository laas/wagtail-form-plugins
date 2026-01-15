"""Step definitions for basic form testing."""

# ruff: noqa: D103, ANN201, PT009

from wagtail.models import Page

from demo.models import FormIndexPage, FormPage

from behave import given
from behave.runner import Context


@given("the form index page exists")
def create_form_index_page(context: Context):
    Page.objects.exclude(slug="root").exclude(slug="home").delete()
    FormIndexPage.create_if_missing(Page.objects.get(slug="home"))
    context.test.assertTrue(FormIndexPage.objects.exists())


@given("a form named '{form_title}' exists")
def create_form_page(context: Context, form_title: str):
    form_index_page = FormIndexPage.objects.first()
    if not form_index_page:
        context.test.fail("FormIndexPage not created")
        return

    form_page = FormPage(title=form_title)
    form_index_page.add_child(instance=form_page)
    form_page.save()
    context.test.assertTrue(FormPage.objects.filter(title=form_title).exists())
