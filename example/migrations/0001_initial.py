# Generated by Django 5.1.2 on 2024-10-18 12:24

import django.core.serializers.json
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail_form_mixins.actions.blocks
import wagtail_form_mixins.actions.models
import wagtail_form_mixins.conditional_fields.blocks
import wagtail_form_mixins.conditional_fields.models
import wagtail_form_mixins.streamfield.models
import wagtail_form_mixins.templating.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True, default='Forms list', help_text='A rich text introduction to be displayed before the list of forms.', verbose_name='Form index page introduction')),
                ('form_title', models.CharField(default='Wagtail forms', help_text='A generic title displayed on all form pages.', max_length=255, verbose_name='Form title')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MyFormSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('unique_response', models.BooleanField(help_text='If checked, the user may fill in the form only once.', verbose_name='Unique response')),
                ('intro', wagtail.fields.RichTextField(blank=True, verbose_name='Form introduction text')),
                ('thank_you_text', wagtail.fields.RichTextField(blank=True, verbose_name='Text displayed after form submission')),
                ('form_fields', wagtail.fields.StreamField([('singleline', 19), ('multiline', 22), ('email', 24), ('number', 28), ('url', 30), ('checkbox', 33), ('checkboxes', 36), ('dropdown', 39), ('multiselect', 41), ('radio', 39), ('date', 43), ('datetime', 45), ('hidden', 47)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-field-block-label', 'help_text': 'Short text describing the field.', 'label': 'Label'}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text displayed below the label to add more information.', 'label': 'Help text', 'required': False}), 2: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Check to make the field not editable by the user.', 'label': 'Disabled', 'required': False}), 3: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', (), {}), 4: ('wagtail.blocks.CharBlock', (), {'help_text': 'Single line text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 5: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the field.', 'label': 'Min length'}), 6: ('wagtail.blocks.IntegerBlock', (), {'default': 255, 'help_text': 'Maximum amount of characters allowed in the field.', 'label': 'Max length'}), 7: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-field', 'validators': [wagtail_form_mixins.conditional_fields.blocks.validate_field]}), 8: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('eq', 'is equal to'), ('neq', 'is not equal to'), ('is', 'is'), ('nis', 'is not'), ('lt', 'is lower than'), ('lte', 'is lower or equal to'), ('ut', 'is upper than'), ('ute', 'is upper or equal to'), ('bt', 'is before than'), ('bte', 'is before or equal to'), ('at', 'is after than'), ('ate', 'is after or equal to'), ('ct', 'contains'), ('nct', 'does not contain'), ('c', 'is checked'), ('nc', 'is not checked')], 'form_classname': 'formbuilder-beb-operator'}), 9: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-val-char', 'required': False}), 10: ('wagtail.blocks.DecimalBlock', (), {'form_classname': 'formbuilder-beb-val-num', 'required': False}), 11: ('wagtail.blocks.CharBlock', (), {'form_classname': 'formbuilder-beb-val-list', 'required': False}), 12: ('wagtail.blocks.DateBlock', (), {'form_classname': 'formbuilder-beb-val-date', 'required': False}), 13: ('wagtail.blocks.StructBlock', [[('field', 7), ('operator', 8), ('value_char', 9), ('value_number', 10), ('value_dropdown', 11), ('value_date', 12)]], {}), 14: ('wagtail.blocks.ListBlock', (13,), {'default': [], 'form_classname': 'formbuilder-beb-rules', 'label': 'Conditions'}), 15: ('wagtail.blocks.StructBlock', [[('field', 7), ('operator', 8), ('value_char', 9), ('value_number', 10), ('value_dropdown', 11), ('value_date', 12), ('rules', 14)]], {}), 16: ('wagtail.blocks.ListBlock', (15,), {'default': [], 'form_classname': 'formbuilder-beb-rules', 'label': 'Conditions'}), 17: ('wagtail.blocks.StructBlock', [[('field', 7), ('operator', 8), ('value_char', 9), ('value_number', 10), ('value_dropdown', 11), ('value_date', 12), ('rules', 16)]], {}), 18: ('wagtail.blocks.ListBlock', (17,), {'default': [], 'form_classname': 'formbuilder-field-block-rule', 'label': 'Visibility condition', 'max_num': 1}), 19: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 4), ('min_length', 5), ('max_length', 6), ('rule', 18)]], {}), 20: ('wagtail.blocks.TextBlock', (), {'help_text': 'Multi-line text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 21: ('wagtail.blocks.IntegerBlock', (), {'default': 1024, 'help_text': 'Maximum amount of characters allowed in the field.', 'label': 'Max length'}), 22: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 20), ('min_length', 5), ('max_length', 21), ('rule', 18)]], {}), 23: ('wagtail.blocks.EmailBlock', (), {'help_text': 'E-mail used to pre-fill the field.', 'label': 'Default value', 'required': False}), 24: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 23), ('rule', 18)]], {}), 25: ('wagtail.blocks.DecimalBlock', (), {'help_text': 'Number used to pre-fill the field.', 'label': 'Default value', 'required': False}), 26: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Minimum number allowed in the field.', 'label': 'Min value', 'required': False}), 27: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Maximum number allowed in the field.', 'label': 'Max value', 'required': False}), 28: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 25), ('min_value', 26), ('max_value', 27), ('rule', 18)]], {}), 29: ('wagtail.blocks.URLBlock', (), {'help_text': 'URL used to pre-fill the field.', 'label': 'Default value', 'required': False}), 30: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 29), ('rule', 18)]], {}), 31: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('the box must be checked',), {}), 32: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'If checked, the box will be checked by default.', 'label': 'Checked', 'required': False}), 33: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 31), ('initial', 32), ('rule', 18)]], {}), 34: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('at least one box must be checked',), {}), 35: ('wagtail_form_mixins.streamfield.blocks.ChoicesList', (wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock(form_classname='formbuilder-choice-label', label='Label')), ('initial', wagtail.blocks.BooleanBlock(label='Checked', required=False))]),), {}), 36: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 34), ('choices', 35), ('rule', 18)]], {}), 37: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('an item must be selected',), {}), 38: ('wagtail_form_mixins.streamfield.blocks.ChoicesList', (), {}), 39: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 37), ('choices', 38), ('rule', 18)]], {}), 40: ('wagtail_form_mixins.streamfield.blocks.RequiredBlock', ('at least one item must be selected',), {}), 41: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 40), ('choices', 38), ('rule', 18)]], {}), 42: ('wagtail.blocks.DateBlock', (), {'help_text': 'Date used to pre-fill the field.', 'label': 'Default value', 'required': False}), 43: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 42), ('rule', 18)]], {}), 44: ('wagtail.blocks.DateTimeBlock', (), {'help_text': 'Date and time used to pre-fill the field.', 'label': 'Default value', 'required': False}), 45: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 44), ('rule', 18)]], {}), 46: ('wagtail.blocks.CharBlock', (), {'help_text': 'Hidden text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 47: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('disabled', 2), ('required', 3), ('initial', 46), ('rule', 18)]], {})}, verbose_name='Form fields')),
                ('emails_to_send', wagtail.fields.StreamField([('email_to_send', 3)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'E-mail addresses of the recipients, separated by comma.', 'label': 'Recipient list', 'validators': [wagtail_form_mixins.actions.blocks.validate_emails]}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'The subject of the e-mail.', 'label': 'Subject'}), 2: ('wagtail.blocks.RichTextBlock', (), {'help_text': 'The body of the e-mail.', 'label': 'Message'}), 3: ('wagtail.blocks.StructBlock', [[('recipient_list', 0), ('subject', 1), ('message', 2)]], {})}, default=[{'type': 'email_to_send', 'value': {'message': 'Bonjour {author.full_name},</p><p>Le {result.publish_date} à {result.publish_time}, l’utilisateur {user.full_name} a complété le formulaire "{form.title}", avec le contenu suivant:</p><p></p><p>{result.data}</p><p></p><p>Bonne journée.', 'recipient_list': '{author.email}', 'subject': 'Nouvelle entrée pour le formulaire "{form.title}"'}}, {'type': 'email_to_send', 'value': {'message': 'Bonjour {user.full_name},</p><p>Vous venez de compléter le formulaire "{form.title}", avec le contenu suivant:</p><p></p><p>{result.data}</p><p></p><p>L’auteur du formulaire en a été informé.</p><p>Bonne journée.', 'recipient_list': '{user.email}', 'subject': 'Confirmation de l’envoi du formulaire "{form.title}"'}}], verbose_name='E-mails to send after form submission')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='example.service', verbose_name='Service')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='example.team', verbose_name='Team')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_form_mixins.actions.models.EmailActionsFormMixin, wagtail_form_mixins.templating.models.TemplatingFormMixin, wagtail_form_mixins.conditional_fields.models.ConditionalFieldsFormMixin, wagtail_form_mixins.streamfield.models.StreamFieldFormMixin, 'wagtailcore.page', models.Model),
        ),
    ]
