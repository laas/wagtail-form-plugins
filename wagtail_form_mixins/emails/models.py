from django.conf import settings

from wagtail.admin.mail import send_mail


class EmailsFormMixin:
    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        for email_block in self.emails_to_send:
            self.send_email(email_block, form)
        return submission

    def before_send(self, email, form):
        return email

    def send_email(self, email_block, form):
        email = {
            "subject": email_block.value["subject"],
            "message": str(email_block.value["message"]),
            "recipient_list": [a.strip() for a in email_block.value["recipient_list"].split(',')],
            "from_email": settings.FORMS_FROM_EMAIL,
        }

        email = self.before_send(email, form)
        print('sending email:', email)
        # send_mail(**email)
