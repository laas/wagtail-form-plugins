# Wagtail Form Plugins

A set of plugins used to customize and improve the Wagtail form builder in a modular way.

This project uses Wagtail StreamFields to improve the user experience when creating a form.
This feature was included in a plugin at first, but moving it to a built-in feature allows a better
integration between plugins and Wagtail StreamFields.

Available plugins:

- **conditional fields**: make a field appear or not depending on the value of a previous field;
- **editable**: allow form admins to modify form submissions;
- **emails**: send multiple emails when a form is submitted;
- **file_input**: allow users to send a file via the form;
- **indexed_results**: add an index value in the results (can be used in the templating plugin);
- **label**: add a new _Label_ field type to put subtitles in forms, in order to split it into sections;
- **named_form**: add user value in form sumission, allowing to fill the form only once per user;
- **nav_buttons**: add some buttons for an easier novigation for form admins;
- **templating**: allow to inject variables in field initial values and emails such as the user name, etc;
- **token_validation**: add token-validation process via email, useful for public forms.

Each plugin is supposed to work independently.

## Usage

You add form plugins with class inheritance.
Since there are several classes to extend, a WagtailFormPlugin object can be used for convenience:

```py
from wagtail_form_plugins import plugins

wfp = WagtailFormPlugin(
    plugins.ConditionalFields,
    plugins.Editable,
    plugins.EmailActions,
    plugins.FileInput,
    plugins.IndexedResults,
    plugins.Label,
    plugins.AuthForm,
    plugins.NavButtons,
    plugins.Templating,
    plugins.Validation,
)

class CustomFormSubmission(*wfp.form_submission_classes):
    pass

class CustomFormBuilder(*wfp.form_builder_classes):
    pass

class CustomFormField(*wfp.form_field_classes):
    pass

class CustomSubmissionListView(*wfp.submission_list_view_classes):
    pass

class CustomFormPage(*wfp.form_page_classes):
    pass

class CustomFormFieldsBlock(*wfp.form_block_classes):
    pass

```

See the `demo` project for further understanding and up-to-date usage.

## Installation

This package is [published on pypi](https://pypi.org/project/wagtail_form_plugins/), so typically:

    uv add wagtail_form_plugins

## Contribution

You are welcome to make pull requests to add you own plugins if you think they can be useful for others.
