"""Common step definitions used in many plugins."""

# ruff: noqa: D103, ANN201, PT009
import logging
import re

from django.core import mail

from demo.tests.environment import Context

from behave import then, use_step_matcher

use_step_matcher("re")

logger = logging.getLogger(__name__)


@then("I should receive an email")
def check_email(context: Context):
    context.test.assertGreater(len(mail.outbox), 0, "no email was sent")
    context.last_email = mail.outbox[-1]  # ty: ignore invalid-assignment


@then(r'the email subject should contain "(?P<text>.+?)"')
def check_email_subject(context: Context, text: str):
    context.test.assertIn(
        text.lower(),
        str(context.last_email.subject).lower(),
        f'text "{text}" not found in email subject "{context.last_email.subject}"',
    )


@then(r"the email should be sent to (?P<recipient>\S+@\S+)")
def check_email_to(context: Context, recipient: str):
    context.test.assertIn(
        recipient,
        context.last_email.to,
        f"recipient {recipient} not found in {context.last_email.to}",
    )


@then(r"the email should be sent from (?P<recipient>\S+@\S+)")
def check_email_from(context: Context, sender: str):
    context.test.assertEqual(
        context.last_email.from_email,
        sender,
        f"expected sender: {sender}, got: {context.last_email.from_email}",
    )


@then(r'the email body should contain "(?P<text>.+?)"')
def check_email_text_body(context: Context, text: str):
    context.test.assertIn(
        text.lower(), str(context.last_email.body).lower(), f'text "{text}" not found in email body'
    )


@then(r'the email html should contain "(?P<text>.+?)"')
def check_email_html_body(context: Context, text: str):
    html_content = ""
    for content, mimetype in context.last_email.alternatives:
        if mimetype == "text/html":
            html_content = str(content)
            break

    context.test.assertIn(text, html_content, f'text "{text}" not found in email HTML')


@then("the email body should contain a link")
def check_link_in_email_body(context: Context):
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    match = re.search(url_pattern, str(context.last_email.body))

    context.test.assertIsNotNone(match, "no link found in email body")
    context.link = match.group(0).rstrip(".,;:!?") if match else ""


@then(r"I dump the email details")
def step_see_email_details(context: Context):
    email = context.last_email
    logger.info("=== EMAIL DETAILS ===")
    logger.info("Subject: %s", email.subject)
    logger.info("From: %s", email.from_email)
    logger.info("To: %s", email.to)
    logger.info("Reply to: %s", email.reply_to)
    logger.info("\nBody (text):\n%s", email.body)

    for content, mimetype in email.alternatives:
        if mimetype == "text/html":
            logger.info("\nBody (html):\n%s", content)
    logger.info("=====================")
