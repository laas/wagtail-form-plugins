TEMPLATE_VAR_LEFT = '{'
TEMPLATE_VAR_RIGHT = '}'


class LazyContext:
    def __init__(self, **kwargs):
        self.values = {}
        self.values_callable = kwargs

    def format(self, message):
        for val_key in self.values_callable.keys():
            look_for = TEMPLATE_VAR_LEFT + val_key + TEMPLATE_VAR_RIGHT
            if look_for in message:
                message = message.replace(look_for, self.get_value(val_key))
        return message

    def get_value(self, key):
        if key not in self.values:
            self.values[key] = self.values_callable[key]()

        return self.values[key]


class FormContext(LazyContext):
    def __init__(self, form):
        super().__init__(
            user=lambda: str(form.user)
        )


class TemplatingFormMixin:
    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)

        if request.method == 'GET':
            form = response.context_data['form']
            form_context = FormContext(form)
            for field in form.fields.values():
                field.initial = form_context.format(field.initial)

        return response

    def before_send(self, email, form):
        form_context = FormContext(form)
        email["subject"] = form_context.format(email["subject"])
        email["message"] = form_context.format(email["message"])
        return email
