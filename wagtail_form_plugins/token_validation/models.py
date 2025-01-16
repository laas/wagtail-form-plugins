import uuid
from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.query import QuerySet

from wagtail.contrib.forms.models import FormMixin, AbstractFormSubmission
from wagtail.contrib.forms.forms import BaseForm
from wagtail.admin.mail import send_mail


class TokenValidationFormSubmission(AbstractFormSubmission):
    token = models.CharField(max_length=255, default="")
    validated = models.BooleanField(default=False)
    email = models.EmailField(default="")

    @classmethod
    def flush(cls, qs: QuerySet) -> int:
        flushed_amount = 0
        for submission in qs.filter(validated=False):
            delay: timedelta = datetime.now(timezone.utc) - submission.submit_time
            if delay.total_seconds() / 60 > settings.FORMS_VALIDATION_EXPIRATION_DELAY:
                submission.delete()
                flushed_amount += 1
        return flushed_amount

    def save(self, *args, **kwargs) -> None:
        if not self.token:
            self.token = str(uuid.uuid4())
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TokenValidationFormMixin(FormMixin):
    # def serve(self, request, *args, **kwargs):
    # if request.method == "POST":
    #     validate_email(request.POST.get("email", ""))

    # return super().serve(request, *args, **kwargs)

    def process_form_submission(self, form: BaseForm):
        submission = super().process_form_submission(form)

        submission.email = form.data["email"]
        submission.save()

        url_params = {
            "submission_id": submission.pk,
            "token": submission.token,
        }
        validation_url = reverse("forms:validate_submission", kwargs=url_params)

        send_mail(
            self.get_email_validation_title(),
            self.get_email_validation_body(validation_url),
            [form.data["email"]],
            settings.DEFAULT_FROM_EMAIL,
        )

    def get_email_validation_title(self) -> str:
        return "Confirm form submission"

    def get_email_validation_body(self, validation_url) -> str:
        return f"Form validation link: { validation_url }"

    class Meta:
        abstract = True
