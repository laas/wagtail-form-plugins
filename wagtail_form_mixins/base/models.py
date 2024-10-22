from django.db import models

# Ressources related to each plugin:
# - FormSubmission
# - CustomSubmissionsListView?
# - FormBuilder
# - FormBlock
# - FormModel
# - hooks


class PluginBase(models.Model):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_submission_options(self, form):
        return {
            "form_data": form.cleaned_data,
            "page": self,
        }

    def process_form_submission(self, form):
        options = self.get_submission_options(form)
        print("options:", options)
        return self.get_submission_class().objects.create(**options)

    class Meta:
        abstract = True