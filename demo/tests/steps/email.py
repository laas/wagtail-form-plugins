"""Step definitions related to emails checks."""

# ruff: noqa: D103, ANN201, PT009
import logging
import re

from django.core import mail
from django.core.mail import EmailMultiAlternatives

from demo.tests.environment import Context

from behave import then, use_step_matcher, when

use_step_matcher("re")

LOGGER = logging.getLogger(__name__)


@when("I send a test email")
def step_test_emails(context: Context):
    email = EmailMultiAlternatives("A test email", "Hello", "from@example.com", ["to@example.com"])
    email_result = email.send()
    context.test.assertEqual(email_result, 1)


@then(r"I should have (?P<amount>\d+) emails? in my mailbox")
def check_emails_amount(context: Context, amount: str):
    context.test.assertEqual(len(mail.outbox), int(amount))


@then("I should receive an email")
def check_email(context: Context):
    context.test.assertGreater(len(mail.outbox), 0, "mailbox is empty")
    context.last_email = mail.outbox.pop()  # ty: ignore invalid-assignment


@then(r'the email subject should contain "(?P<text>.+?)"')
def check_email_subject(context: Context, text: str):
    expected = text.lower()
    actual = str(context.last_email.subject).lower()
    context.test.assertIn(expected, actual)


@then(r"the email should be sent to (?P<recipient>\S+@\S+)")
def check_email_to(context: Context, recipient: str):
    context.test.assertIn(recipient, context.last_email.to)


@then(r"the email should be sent from (?P<recipient>\S+@\S+)")
def check_email_from(context: Context, sender: str):
    context.test.assertEqual(context.last_email.from_email, sender)


@then(r'the email body should (h?P<neg>not )contain "(?P<text>.+?)"')
def check_email_text_body(context: Context, text: str, neg: str = ""):
    expected = text.lower()
    actual = str(context.last_email.body).lower()
    assert_func = context.test.assertNotIn if neg == "not" else context.test.assertIn
    assert_func(expected, actual)


@then(r'the email html should (h?P<neg>not )contain "(?P<text>.+?)"')
def check_email_html_body(context: Context, text: str, neg: str = ""):
    expected = text.lower()
    actual = ""
    for content, mimetype in context.last_email.alternatives:
        if mimetype == "text/html":
            actual = str(content).lower()
            break
    assert_func = context.test.assertNotIn if neg == "not" else context.test.assertIn
    assert_func(expected, actual)


@then("the email body should contain a link")
def check_link_in_email_body(context: Context):
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    match = re.search(url_pattern, str(context.last_email.body))

    context.test.assertIsNotNone(match, "no link found in email body")
    context.link = match.group(0).rstrip(".,;:!?") if match else ""


@then(r"I dump the email details")
def step_see_email_details(context: Context):
    email = context.last_email
    LOGGER.info("=== EMAIL DETAILS ===")
    LOGGER.info("Subject: %s", email.subject)
    LOGGER.info("From: %s", email.from_email)
    LOGGER.info("To: %s", email.to)
    LOGGER.info("Reply to: %s", email.reply_to)
    LOGGER.info("\nBody (text):\n%s", email.body)

    for content, mimetype in email.alternatives:
        if mimetype == "text/html":
            LOGGER.info("\nBody (html):\n%s", content)
    LOGGER.info("=====================")
