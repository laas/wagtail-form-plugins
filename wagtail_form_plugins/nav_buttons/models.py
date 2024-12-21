from wagtail_form_plugins.base.models import FormMixin


class NavButtonsFormMixin(FormMixin):
    def submissions_amount(self):
        return self.get_submission_class().objects.filter(page=self).count()

    class Meta:
        abstract = True
