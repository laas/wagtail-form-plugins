import json

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import FormMixin
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.admin.mail import send_mail

from .forms import StreamFieldFormBuilder


class StreamFieldFormMixin(FormMixin):
    """A mixin that adds form builder functionality to the page."""

    form_builder = StreamFieldFormBuilder

    def get_form_fields(self):
        return self.form_fields

    def get_data_fields(self):
        data_fields = [
            ("submit_time", _("Submission date")),
        ]

        data_fields += [
            (get_field_clean_name(data["value"]["label"]), data["value"]["label"])
            for data in self.get_form_fields().raw_data
        ]

        return data_fields

    @classmethod
    def get_visibility_conditions(cls, fields_id, visibility_conditions):
        conditions = []
        for vc in visibility_conditions:
            if vc["type"] in ("bool_and", "bool_or"):
                vc_block = cls.get_visibility_conditions(fields_id, vc["value"])
                conditions.append({vc["type"][5:]: vc_block})
            else:
                vc["value"]["field_id"] = fields_id[vc["value"]["field_id"]]
                conditions.append(vc["value"])

        return [{}] if not conditions else conditions

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)
        form = form_class(*args, **form_params)

        raw_data = form_params["page"].form_fields.raw_data
        fields_data = {
            get_field_clean_name(fd["value"]["label"]): fd for fd in raw_data
        }

        dom_ids = {fields_data[id]["id"]: f"id_{id}" for id in form.fields.keys()}

        for name, field in form.fields.items():
            raw_vc = fields_data[name]["value"]["visibility_condition"]
            vc = self.get_visibility_conditions(dom_ids, raw_vc)[0]
            field.widget.attrs.update(
                {
                    "data-vc": json.dumps(vc),
                    "class": "form-control",
                }
            )

        return form


class EmailsFormMixin(models.Model):
    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        for email_block in self.emails_to_send:
            self.send_email(email_block)
        return submission

    def send_email(self, email_block):
        email = {
            "subject": email_block.value["subject"],
            "message": str(email_block.value["message"]),
            "recipient_list": [a.strip() for a in email_block.value["recipient_list"].split(',')],
            "from_email": settings.FORMS_FROM_EMAIL,
        }

        print('sending email:', email)
        # send_mail(**email)

    class Meta:
        abstract = True
