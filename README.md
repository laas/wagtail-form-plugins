# Wagtail Form mixins

A set a mixins used to add features to Wagtail forms:

- **actions**: trigger actions when a form is submitted - mainly used to send emails for now;
- **conditional fields**: make a field appear or not depending on the value of a previous field;
- **streamfield**: improve the user experience of the form app, using StreamFields __*__.
- **templating**: allow to inject variables in field initial values and emails such as the user name, etc.

> __*__ Note: this feature has been suggested to Wagtail core on
[this pull request](https://github.com/wagtail/wagtail/pull/12287) and will be probably removed from
this project once a StreamField-based form will be included in Wagtail.
