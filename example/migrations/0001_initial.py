# Generated by Django 5.1.1 on 2024-09-09 08:06

import django.db.models.deletion
import forms.models
import wagtail.contrib.forms.models
import wagtail.fields
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
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address')),
                ('from_address', models.EmailField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('form_fields', wagtail.fields.StreamField([('singleline', 15), ('multiline', 19), ('email', 21), ('number', 25), ('url', 27), ('checkbox', 29), ('checkboxes', 34), ('dropdown', 38), ('multiselect', 38), ('radio', 38), ('date', 40), ('datetime', 42), ('hidden', 43)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text describing the field.'}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text displayed below the label used to add more information, like this one.', 'required': False}), 2: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'If checked, this field must be filled to validate the form.', 'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'form_classname': 'form-block-hidden', 'required': False}), 4: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('eq', 'equals'), ('neq', 'not equals')]}), 5: ('wagtail.blocks.CharBlock', (), {}), 6: ('wagtail.blocks.StructBlock', [[('field_label', 3), ('field_id', 3), ('operator', 4), ('value', 5)]], {'group': ' Fields'}), 7: ('wagtail.blocks.StreamBlock', [[('cond_1', 6), ('cond_2', 6), ('cond_3', 6), ('cond_4', 6), ('cond_5', 6), ('cond_6', 6), ('cond_7', 6), ('cond_8', 6), ('cond_9', 6), ('cond_10', 6), ('cond_11', 6), ('cond_12', 6), ('cond_13', 6), ('cond_14', 6), ('cond_15', 6), ('cond_16', 6), ('cond_17', 6), ('cond_18', 6), ('cond_19', 6), ('cond_20', 6), ('cond_21', 6), ('cond_22', 6), ('cond_23', 6), ('cond_24', 6), ('cond_25', 6), ('cond_26', 6), ('cond_27', 6), ('cond_28', 6), ('cond_29', 6), ('cond_30', 6), ('cond_31', 6), ('cond_32', 6), ('cond_33', 6), ('cond_34', 6), ('cond_35', 6), ('cond_36', 6), ('cond_37', 6), ('cond_38', 6), ('cond_39', 6), ('cond_40', 6), ('cond_41', 6), ('cond_42', 6), ('cond_43', 6), ('cond_44', 6), ('cond_45', 6), ('cond_46', 6), ('cond_47', 6), ('cond_48', 6), ('cond_49', 6), ('cond_50', 6)]], {'label': 'AND', 'max_num': 6, 'min_num': 2}), 8: ('wagtail.blocks.StreamBlock', [[('cond_1', 6), ('cond_2', 6), ('cond_3', 6), ('cond_4', 6), ('cond_5', 6), ('cond_6', 6), ('cond_7', 6), ('cond_8', 6), ('cond_9', 6), ('cond_10', 6), ('cond_11', 6), ('cond_12', 6), ('cond_13', 6), ('cond_14', 6), ('cond_15', 6), ('cond_16', 6), ('cond_17', 6), ('cond_18', 6), ('cond_19', 6), ('cond_20', 6), ('cond_21', 6), ('cond_22', 6), ('cond_23', 6), ('cond_24', 6), ('cond_25', 6), ('cond_26', 6), ('cond_27', 6), ('cond_28', 6), ('cond_29', 6), ('cond_30', 6), ('cond_31', 6), ('cond_32', 6), ('cond_33', 6), ('cond_34', 6), ('cond_35', 6), ('cond_36', 6), ('cond_37', 6), ('cond_38', 6), ('cond_39', 6), ('cond_40', 6), ('cond_41', 6), ('cond_42', 6), ('cond_43', 6), ('cond_44', 6), ('cond_45', 6), ('cond_46', 6), ('cond_47', 6), ('cond_48', 6), ('cond_49', 6), ('cond_50', 6)]], {'label': 'OR', 'max_num': 6, 'min_num': 2}), 9: ('wagtail.blocks.StreamBlock', [[('bool_and', 7), ('bool_or', 8), ('cond_1', 6), ('cond_2', 6), ('cond_3', 6), ('cond_4', 6), ('cond_5', 6), ('cond_6', 6), ('cond_7', 6), ('cond_8', 6), ('cond_9', 6), ('cond_10', 6), ('cond_11', 6), ('cond_12', 6), ('cond_13', 6), ('cond_14', 6), ('cond_15', 6), ('cond_16', 6), ('cond_17', 6), ('cond_18', 6), ('cond_19', 6), ('cond_20', 6), ('cond_21', 6), ('cond_22', 6), ('cond_23', 6), ('cond_24', 6), ('cond_25', 6), ('cond_26', 6), ('cond_27', 6), ('cond_28', 6), ('cond_29', 6), ('cond_30', 6), ('cond_31', 6), ('cond_32', 6), ('cond_33', 6), ('cond_34', 6), ('cond_35', 6), ('cond_36', 6), ('cond_37', 6), ('cond_38', 6), ('cond_39', 6), ('cond_40', 6), ('cond_41', 6), ('cond_42', 6), ('cond_43', 6), ('cond_44', 6), ('cond_45', 6), ('cond_46', 6), ('cond_47', 6), ('cond_48', 6), ('cond_49', 6), ('cond_50', 6)]], {'label': 'AND', 'max_num': 6, 'min_num': 2}), 10: ('wagtail.blocks.StreamBlock', [[('bool_and', 7), ('bool_or', 8), ('cond_1', 6), ('cond_2', 6), ('cond_3', 6), ('cond_4', 6), ('cond_5', 6), ('cond_6', 6), ('cond_7', 6), ('cond_8', 6), ('cond_9', 6), ('cond_10', 6), ('cond_11', 6), ('cond_12', 6), ('cond_13', 6), ('cond_14', 6), ('cond_15', 6), ('cond_16', 6), ('cond_17', 6), ('cond_18', 6), ('cond_19', 6), ('cond_20', 6), ('cond_21', 6), ('cond_22', 6), ('cond_23', 6), ('cond_24', 6), ('cond_25', 6), ('cond_26', 6), ('cond_27', 6), ('cond_28', 6), ('cond_29', 6), ('cond_30', 6), ('cond_31', 6), ('cond_32', 6), ('cond_33', 6), ('cond_34', 6), ('cond_35', 6), ('cond_36', 6), ('cond_37', 6), ('cond_38', 6), ('cond_39', 6), ('cond_40', 6), ('cond_41', 6), ('cond_42', 6), ('cond_43', 6), ('cond_44', 6), ('cond_45', 6), ('cond_46', 6), ('cond_47', 6), ('cond_48', 6), ('cond_49', 6), ('cond_50', 6)]], {'label': 'OR', 'max_num': 6, 'min_num': 2}), 11: ('wagtail.blocks.StreamBlock', [[('bool_and', 9), ('bool_or', 10), ('cond_1', 6), ('cond_2', 6), ('cond_3', 6), ('cond_4', 6), ('cond_5', 6), ('cond_6', 6), ('cond_7', 6), ('cond_8', 6), ('cond_9', 6), ('cond_10', 6), ('cond_11', 6), ('cond_12', 6), ('cond_13', 6), ('cond_14', 6), ('cond_15', 6), ('cond_16', 6), ('cond_17', 6), ('cond_18', 6), ('cond_19', 6), ('cond_20', 6), ('cond_21', 6), ('cond_22', 6), ('cond_23', 6), ('cond_24', 6), ('cond_25', 6), ('cond_26', 6), ('cond_27', 6), ('cond_28', 6), ('cond_29', 6), ('cond_30', 6), ('cond_31', 6), ('cond_32', 6), ('cond_33', 6), ('cond_34', 6), ('cond_35', 6), ('cond_36', 6), ('cond_37', 6), ('cond_38', 6), ('cond_39', 6), ('cond_40', 6), ('cond_41', 6), ('cond_42', 6), ('cond_43', 6), ('cond_44', 6), ('cond_45', 6), ('cond_46', 6), ('cond_47', 6), ('cond_48', 6), ('cond_49', 6), ('cond_50', 6)]], {}), 12: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text used to pre-fill the field.', 'label': 'Default value', 'required': False}), 13: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the field.'}), 14: ('wagtail.blocks.IntegerBlock', (), {'default': 255, 'help_text': 'Maximum amount of characters allowed in the field.'}), 15: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 12), ('min_length', 13), ('max_length', 14)]], {}), 16: ('wagtail.blocks.TextBlock', (), {'help_text': 'Multi-line text used to pre-fill the text area.', 'label': 'Default value', 'required': False}), 17: ('wagtail.blocks.IntegerBlock', (), {'default': 0, 'help_text': 'Minimum amount of characters allowed in the text area.'}), 18: ('wagtail.blocks.IntegerBlock', (), {'default': 1024, 'help_text': 'Maximum amount of characters allowed in the text area.'}), 19: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 16), ('min_length', 17), ('max_length', 18)]], {}), 20: ('wagtail.blocks.EmailBlock', (), {'help_text': 'E-mail used to pre-fill the field.', 'label': 'Default value', 'required': False}), 21: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 20)]], {}), 22: ('wagtail.blocks.DecimalBlock', (), {'help_text': 'Number used to pre-fill the field.', 'label': 'Default value', 'required': False}), 23: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Minimum number allowed in the field.', 'required': False}), 24: ('wagtail.blocks.IntegerBlock', (), {'help_text': 'Maximum number allowed in the field.', 'required': False}), 25: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 22), ('min_value', 23), ('max_value', 24)]], {}), 26: ('wagtail.blocks.URLBlock', (), {'help_text': 'URL used to pre-fill the field.', 'label': 'Default value', 'required': False}), 27: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 26)]], {}), 28: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'If checked, the checkbox will be checked by default.', 'label': 'Checked', 'required': False}), 29: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 28)]], {}), 30: ('wagtail.blocks.CharBlock', (), {'label': 'Label'}), 31: ('wagtail.blocks.BooleanBlock', (), {'label': 'Checked', 'required': False}), 32: ('wagtail.blocks.StructBlock', [[('label', 30), ('initial', 31)]], {}), 33: ('wagtail.blocks.ListBlock', (32,), {'label': 'Choices'}), 34: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('choices', 33)]], {}), 35: ('wagtail.blocks.BooleanBlock', (), {'label': 'Selected', 'required': False}), 36: ('wagtail.blocks.StructBlock', [[('label', 30), ('initial', 35)]], {}), 37: ('wagtail.blocks.ListBlock', (36,), {'label': 'Choices'}), 38: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('choices', 37)]], {}), 39: ('wagtail.blocks.DateBlock', (), {'help_text': 'Date used to pre-fill the field.', 'label': 'Default value', 'required': False}), 40: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 39)]], {}), 41: ('wagtail.blocks.DateTimeBlock', (), {'help_text': 'Date/time used to pre-fill the field.', 'label': 'Default value', 'required': False}), 42: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 41)]], {}), 43: ('wagtail.blocks.StructBlock', [[('label', 0), ('help_text', 1), ('required', 2), ('visibility_condition', 11), ('initial', 12)]], {})})),
                ('thank_you_text', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(forms.models.StreamFieldFormMixin, 'wagtailcore.page', models.Model),
        ),
    ]
