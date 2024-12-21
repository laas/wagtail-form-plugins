# Wagtail form mixins

A set of mixins used to customise and improve Wagtail forms in a modular way.

- **streamfield**: improve the user experience of the form app, using StreamFields;
- **conditional fields**: make a field appear or not depending on the value of a previous field;
- **templating**: allow to inject variables in field initial values and emails such as the user name, etc;
- **file_input**: allow users to send a file via the form;
- **indexed_results**: add an index in the results (can be used in the templating plugin);
- **named_form**: allow to fill the form only once per user;
- **emails**: send multiple emails when a form is submitted;
- **datepickers**: add `date` and `datetime` input types to make the browser datepicker appear;

Each of them is supposed to work independently. See the `example` folder to understand how to use it.

You are welcome to make pull requests to add you own plugins if you think they can be useful for others.

This project is currently in beta: feedback is more than welcome, expect some API-breaks in minor releases.
