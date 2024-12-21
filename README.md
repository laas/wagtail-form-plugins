# Wagtail Form Plugins

A set of plugins used to customize and improve the Wagtail form builder in a modular way.

- **streamfield**: improve the user experience of the form app, using StreamFields;
- **conditional fields**: make a field appear or not depending on the value of a previous field;
- **templating**: allow to inject variables in field initial values and emails such as the user name, etc;
- **file_input**: allow users to send a file via the form;
- **indexed_results**: add an index in the results (can be used in the templating plugin);
- **named_form**: allow to fill the form only once per user;
- **emails**: send multiple emails when a form is submitted;
- **datepickers**: add `date` and `datetime` input types to make the browser datepicker appear.

Each plugin is supposed to work independently.

## Usage

Plugins are Python mixins, you add them with class inheritance:

```py
from wagtail_form_plugins import models as wfp_models

class AbstractFormPage(
    wfp_models.TemplatingFormMixin,
    wfp_models.FileInputFormMixin,
    wfp_models.ConditionalFieldsFormMixin,
    wfp_models.StreamFieldFormMixin,
    wfp_models.NavButtonsFormMixin,
    wfp_models.IndexedResultsFormMixin,
    FormMixin,
    Page,
):
```

See the `demo` project for further understanding.

## Installation

This package is [published on pypi](https://pypi.org/project/wagtail_form_plugins/):

    poetry add wagtail_form_plugins

or:

    pip install wagtail_form_plugins

## Contribution

You are welcome to make pull requests to add you own plugins if you think they can be useful for others.

This project is currently in beta: feedback is more than welcome, expect some API-breaks in minor releases.
