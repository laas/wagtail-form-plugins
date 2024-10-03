# Generated by Django 5.1.1 on 2024-10-03 13:36

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail_form_mixins.actions.blocks
import wagtail_form_mixins.actions.models
import wagtail_form_mixins.conditional_fields.blocks
import wagtail_form_mixins.conditional_fields.models
import wagtail_form_mixins.streamfield.models
import wagtail_form_mixins.templating.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True, verbose_name="Texte d'introduction du formulaire")),
                ('thank_you_text', wagtail.fields.RichTextField(blank=True, verbose_name='Texte affiché après soumission du formulaire')),
                ('form_fields', wagtail.fields.StreamField([('singleline', 18), ('multiline', 21), ('email', 23), ('number', 27), ('url', 29), ('checkbox', 32), ('checkboxes', 35), ('dropdown', 38), ('multiselect', 40), ('radio', 38), ('date', 42), ('datetime', 44), ('hidden', 46)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-field-block-label', 'help_text': 'Short text describing the field.', 'label': 'Label'}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text displayed below the label to add more information.', 'label': 'Help text', 'required': False}), 2: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', (), {}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': 'Single line text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 4: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the field.', 'label': 'Min length'}), 5: ('wagtail.blocks.IntegerBlock', (), {'default': 255, 'help_text': 'Maximum amount of characters allowed in the field.', 'label': 'Max length'}), 6: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-field', 'validators': [wagtail_form_mixins.conditional_fields.blocks.validate_field]}), 7: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('eq', 'is equal to'), ('neq', 'is not equal to'), ('is', 'is'), ('nis', 'is not'), ('lt', 'is lower than'), ('lte', 'is lower or equal to'), ('ut', 'is upper than'), ('ute', 'is upper or equal to'), ('bt', 'is before than'), ('bte', 'is before or equal to'), ('at', 'is after than'), ('ate', 'is after or equal to'), ('ct', 'contains'), ('nct', 'does not contain'), ('c', 'is checked'), ('nc', 'is not checked')], 'form_classname': 'formbuilder-beb-operator'}), 8: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-val-char', 'required': False}), 9: ('wagtail.blocks.DecimalBlock', (), {'form_classname': 'formbuilder-beb-val-num', 'required': False}), 10: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-val-list', 'required': False}), 11: ('wagtail.blocks.DateBlock', (), {'form_classname': 'formbuilder-beb-val-date', 'required': False}), 12: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 7), ('value_char', 8), ('value_number', 9), ('value_dropdown', 10), ('value_date', 11)]], {}), 13: ('wagtail.blocks.ListBlock', (12,), {'default': [], 'form_classname': 'formbuilder-beb-rules', 'label': 'Conditions'}), 14: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 7), ('value_char', 8), ('value_number', 9), ('value_dropdown', 10), ('value_date', 11), ('rules', 13)]], {}), 15: ('wagtail.blocks.ListBlock', (14,), {'default': [], 'form_classname': 'formbuilder-beb-rules', 'label': 'Conditions'}), 16: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 7), ('value_char', 8), ('value_number', 9), ('value_dropdown', 10), ('value_date', 11), ('rules', 15)]], {}), 17: ('wagtail.blocks.ListBlock', (16,), {'default': [], 'form_classname': 'formbuilder-field-block-rule', 'label': 'Visibility condition', 'max_num': 1}), 18: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 3), ('min_length', 4), ('max_length', 5), ('rule', 17)]], {}), 19: ('wagtail.blocks.TextBlock', (), {'help_text': 'Multi-line text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 20: ('wagtail.blocks.IntegerBlock', (), {'default': 1024, 'help_text': 'Maximum amount of characters allowed in the field.', 'label': 'Max length'}), 21: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 19), ('min_length', 4), ('max_length', 20), ('rule', 17)]], {}), 22: ('wagtail.blocks.EmailBlock', (), {'help_text': 'E-mail used to pre-fill the field.', 'label': 'Default value', 'required': False}), 23: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 22), ('rule', 17)]], {}), 24: ('wagtail.blocks.DecimalBlock', (), {'help_text': 'Number used to pre-fill the field.', 'label': 'Default value', 'required': False}), 25: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Minimum number allowed in the field.', 'label': 'Min value', 'required': False}), 26: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Maximum number allowed in the field.', 'label': 'Max value', 'required': False}), 27: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 24), ('min_value', 25), ('max_value', 26), ('rule', 17)]], {}), 28: ('wagtail.blocks.URLBlock', (), {'help_text': 'URL used to pre-fill the field.', 'label': 'Default value', 'required': False}), 29: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 28), ('rule', 17)]], {}), 30: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('the box must be checked',), {}), 31: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'If checked, the box will be checked by default.', 'label': 'Checked', 'required': False}), 32: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 30), ('initial', 31), ('rule', 17)]], {}), 33: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('at least one box must be checked',), {}), 34: ('wagtail_form_mixins.streamfield.blocks.ChoicesList', (wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock(form_classname='formbuilder-choice-label', label='Label')), ('initial', wagtail.blocks.BooleanBlock(label='Checked', required=False))]),), {}), 35: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 33), ('choices', 34), ('rule', 17)]], {}), 36: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('an item must be selected',), {}), 37: ('wagtail_form_mixins.streamfield.blocks.ChoicesList', (), {}), 38: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 36), ('choices', 37), ('rule', 17)]], {}), 39: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('at least one item must be selected',), {}), 40: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 39), ('choices', 37), ('rule', 17)]], {}), 41: ('wagtail.blocks.DateBlock', (), {'help_text': 'Date used to pre-fill the field.', 'label': 'Default value', 'required': False}), 42: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 41), ('rule', 17)]], {}), 43: ('wagtail.blocks.DateTimeBlock', (), {'help_text': 'Date and time used to pre-fill the field.', 'label': 'Default value', 'required': False}), 44: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 43), ('rule', 17)]], {}), 45: ('wagtail.blocks.CharBlock', (), {'help_text': 'Hidden text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 46: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 45), ('rule', 17)]], {})}, verbose_name='Champs du formulaire')),
                ('emails_to_send', wagtail.fields.StreamField([('email_to_send', 3)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'E-mail addresses of the recipients, separated by comma.', 'label': 'Recipient list', 'validators': [wagtail_form_mixins.actions.blocks.validate_emails]}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'The subject of the e-mail.', 'label': 'Subject'}), 2: ('wagtail.blocks.RichTextBlock', (), {'help_text': 'The body of the e-mail.', 'label': 'Message'}), 3: ('wagtail.blocks.StructBlock', [[('recipient_list', 0), ('subject', 1), ('message', 2)]], {})}, default=[{'type': 'email_to_send', 'value': {'message': 'Bonjour,</p><p>Le formulaire "{title}" vient d\'être complété par l’utilisateur {user.full_name}, avec le contenu suivant:</p><p>{form_results}</p><p>Bonne journée.', 'recipient_list': '{author_email}', 'subject': 'Nouvelle entrée pour le formulaire "{title}"'}}, {'type': 'email_to_send', 'value': {'message': 'Bonjour,</p><p>Vous venez de compléter le formulaire "{title}", avec le contenu suivant:</p><p>{form_results}</p><p>L’auteur du formulaire en a été informé.</p><p>Bonne journée.', 'recipient_list': '{user_email}', 'subject': 'Confirmation de l’envoi du formulaire "{title}"'}}])),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_form_mixins.templating.models.TemplatingFormMixin, wagtail_form_mixins.actions.models.EmailActionsFormMixin, wagtail_form_mixins.conditional_fields.models.ConditionalFieldsFormMixin, wagtail_form_mixins.streamfield.models.StreamFieldFormMixin, 'wagtailcore.page'),
        ),
    ]
