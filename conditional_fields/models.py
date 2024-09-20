import json

from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.models import FormMixin
from wagtail.contrib.forms.utils import get_field_clean_name


class ConditionalFieldsMixin(FormMixin):
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

        # --- WIP ---

        raw_data = form_params["page"].form_fields.raw_data
        fields_data = {
            get_field_clean_name(fd["value"]["label"]): fd for fd in raw_data
        }

        dom_ids = {fields_data[id]["id"]: f"id_{id}" for id in form.fields.keys()}

        for name, field in form.fields.items():
            raw_vc = fields_data[name]["value"]["rules"]
            vc = self.get_visibility_conditions(dom_ids, raw_vc)[0]
            field.widget.attrs.update(
                {
                    "data-vc": json.dumps(vc),
                    "class": "form-control",
                }
            )

        return form

    def get_form_fields(self):
        for ff in self.form_fields.raw_data:
            del ff["value"]["rules"]

        return self.form_fields
