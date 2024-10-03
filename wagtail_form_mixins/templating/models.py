TEMPLATE_VAR_LEFT = '{'
TEMPLATE_VAR_RIGHT = '}'


class LazyContext:
    def __init__(self, **kwargs):
        self.values = {}
        self.values_callable = {}

        for val_name, value in kwargs.items():
            if isinstance(value, dict):
                for sub_val_name, sub_value in value.items():
                    self.values_callable[f'{val_name}.{sub_val_name}'] = sub_value
            else:
                self.values_callable[val_name] = value

    def format(self, message):
        for val_key in self.values_callable.keys():
            look_for = TEMPLATE_VAR_LEFT + val_key + TEMPLATE_VAR_RIGHT
            if look_for in message:
                message = message.replace(look_for, self.get_value(val_key))
        return message

    def get_value(self, key):
        if key not in self.values:
            self.values[key] = str(self.values_callable[key]())

        return self.values[key]


class FormContext(LazyContext):
    def __init__(self, form):
        user = {
            "login": lambda: form.user.username,
            "first_name": lambda: form.user.first_name,
            "last_name": lambda: form.user.last_name,
            "full_name": lambda: f'{form.user.first_name} {form.user.last_name}',
            "email": lambda: form.user.email,
        }

        super().__init__(user=user)


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
