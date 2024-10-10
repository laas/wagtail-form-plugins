from django.conf import settings
from django.utils.html import strip_tags

from wagtail.admin.mail import send_mail


class EmailActionsFormMixin:
    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)

        if "form_submission" in response.context_data:
            for email in response.context_data["page"].emails_to_send:
                self.send_email(email.value)

        return response

    def send_email(self, email):
        send_mail(
            subject=email["subject"],
            message=strip_tags(email["message"].replace("</p>", "</p>\n")),
            recipient_list=[a.strip() for a in email["recipient_list"].split(",")],
            from_email=settings.FORMS_FROM_EMAIL,
            html_message=email["message"],
        )
