# Generated by Django 5.1.1 on 2024-09-17 12:26

import django.db.models.deletion
import wagtail.fields
import wagtail_laas_forms.blocks
import wagtail_laas_forms.models
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
                ('form_fields', wagtail.fields.StreamField([('singleline', 16), ('multiline', 20), ('email', 22), ('number', 26), ('url', 28), ('checkbox', 30), ('checkboxes', 35), ('dropdown', 39), ('multiselect', 39), ('radio', 39), ('date', 41), ('datetime', 43), ('hidden', 44)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-field-block-label', 'help_text': 'Short text describing the field.', 'label': 'Label'}), 1: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-field-block-help', 'help_text': 'Text displayed below the label to add more information.', 'label': 'Help text', 'required': False}), 2: ('wagtail.blocks.BooleanBlock', (), {'form_classname': 'formbuilder-field-block-required', 'help_text': 'If checked, this field must be filled to validate the form.', 'label': 'Required', 'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 4: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the field.', 'label': 'Min length'}), 5: ('wagtail.blocks.IntegerBlock', (), {'default': 255, 'help_text': 'Maximum amount of characters allowed in the field.', 'label': 'Max length'}), 6: ('wagtail.blocks.ChoiceBlock', [], {'choices': []}), 7: ('wagtail.blocks.CharBlock', (), {}), 8: ('wagtail.blocks.DecimalBlock', (), {}), 9: ('wagtail.blocks.DateBlock', (), {}), 10: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 6), ('value_char', 7), ('value_number', 8), ('value_dropdown', 6), ('value_date', 9)]], {}), 11: ('wagtail.blocks.ListBlock', (10,), {'label': 'Conditions', 'min_num': 2}), 12: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 6), ('value_char', 7), ('value_number', 8), ('value_dropdown', 6), ('value_date', 9), ('rules', 11)]], {}), 13: ('wagtail.blocks.ListBlock', (12,), {'label': 'Conditions', 'min_num': 2}), 14: ('wagtail.blocks.StructBlock', [[('field', 6), ('operator', 6), ('value_char', 7), ('value_number', 8), ('value_dropdown', 6), ('value_date', 9), ('rules', 13)]], {}), 15: ('wagtail.blocks.ListBlock', (14,), {'collapsed': True, 'form_classname': 'formbuilder-unique-listblock', 'label': 'Visibility condition'}), 16: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 3), ('min_length', 4), ('max_length', 5), ('rule', 15)]], {}), 17: ('wagtail.blocks.TextBlock', (), {'help_text': 'Multi-line text used to pre-fill the text area.', 'label': 'Default value', 'required': False}), 18: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the text area.', 'label': 'Min length'}), 19: ('wagtail.blocks.IntegerBlock', (), {'default': 1024, 'help_text': 'Maximum amount of characters allowed in the text area.', 'label': 'Max length'}), 20: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 17), ('min_length', 18), ('max_length', 19), ('rule', 15)]], {}), 21: ('wagtail.blocks.EmailBlock', (), {'help_text': 'E-mail used to pre-fill the field.', 'label': 'Default value', 'required': False}), 22: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 21), ('rule', 15)]], {}), 23: ('wagtail.blocks.DecimalBlock', (), {'help_text': 'Number used to pre-fill the field.', 'label': 'Default value', 'required': False}), 24: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Minimum number allowed in the field.', 'label': 'Min value', 'required': False}), 25: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Maximum number allowed in the field.', 'label': 'Max value', 'required': False}), 26: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 23), ('min_value', 24), ('max_value', 25), ('rule', 15)]], {}), 27: ('wagtail.blocks.URLBlock', (), {'help_text': 'URL used to pre-fill the field.', 'label': 'Default value', 'required': False}), 28: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 27), ('rule', 15)]], {}), 29: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'If checked, the checkbox will be checked by default.', 'label': 'Checked', 'required': False}), 30: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 29), ('rule', 15)]], {}), 31: ('wagtail.blocks.CharBlock', (), {'label': 'Label'}), 32: ('wagtail.blocks.BooleanBlock', (), {'label': 'Checked', 'required': False}), 33: ('wagtail.blocks.StructBlock', [[('label', 31), ('initial', 32)]], {}), 34: ('wagtail.blocks.ListBlock', (33,), {'label': 'Choices'}), 35: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('choices', 34), ('rule', 15)]], {}), 36: ('wagtail.blocks.BooleanBlock', (), {'label': 'Selected', 'required': False}), 37: ('wagtail.blocks.StructBlock', [[('label', 31), ('initial', 36)]], {}), 38: ('wagtail.blocks.ListBlock', (37,), {'label': 'Choices'}), 39: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('choices', 38), ('rule', 15)]], {}), 40: ('wagtail.blocks.DateBlock', (), {'help_text': 'Date used to pre-fill the field.', 'label': 'Default value', 'required': False}), 41: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 40), ('rule', 15)]], {}), 42: ('wagtail.blocks.DateTimeBlock', (), {'help_text': 'Date and time used to pre-fill the field.', 'label': 'Default value', 'required': False}), 43: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 42), ('rule', 15)]], {}), 44: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('initial', 3), ('rule', 15)]], {})}, verbose_name='Champs du formulaire')),
                ('emails_to_send', wagtail.fields.StreamField([('email_to_send', 3)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'E-mail addresses of the recipients, separated by comma.', 'label': 'Recipient list', 'validators': [wagtail_laas_forms.blocks.validate_emails]}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'The subject of the e-mail.', 'label': 'Subject'}), 2: ('wagtail.blocks.RichTextBlock', (), {'help_text': 'The body of the e-mail.', 'label': 'Message'}), 3: ('wagtail.blocks.StructBlock', [[('recipient_list', 0), ('subject', 1), ('message', 2)]], {})}, default=[{'type': 'email_to_send', 'value': {'message': '</p><p>Bonjour,</p><p>Le formulaire "{title}" vient d\'être complété par l\'utilisateur {user}, avec le contenu suivant:</p><p>{form_results}</p><p>Bonne journée.', 'recipient_list': '{author_email}', 'subject': 'Nouvelle entrée pour le formulaire "{title}"'}}, {'type': 'email_to_send', 'value': {'message': '</p><p>Bonjour,</p><p>Vous venez de compléter le formulaire "{title}", avec le contenu suivant:</p><p>{form_results}</p><p>L\'auteur du formulaire en a été informé.</p><p>Bonne journée.', 'recipient_list': '{user_email}', 'subject': 'Submission confirmation to the form "{title}"'}}], verbose_name='E-mails à envoyer après soumission du formulaire')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_laas_forms.models.StreamFieldFormMixin, 'wagtailcore.page', models.Model),
        ),
    ]
