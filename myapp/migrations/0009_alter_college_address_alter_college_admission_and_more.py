# Generated by Django 5.0.2 on 2024-02-13 10:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_collegecourse_eligibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='address',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='college',
            name='admission',
            field=ckeditor.fields.RichTextField(default='admission formalities here', max_length=500),
        ),
        migrations.AlterField(
            model_name='college',
            name='affiliation',
            field=ckeditor.fields.RichTextField(default='Affiliation details here', max_length=500),
        ),
        migrations.AlterField(
            model_name='college',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='college',
            name='overview',
            field=ckeditor.fields.RichTextField(default='course overview here', max_length=900),
        ),
        migrations.AlterField(
            model_name='collegecourse',
            name='syllabus',
            field=ckeditor.fields.RichTextField(default='Syllabus here'),
        ),
    ]
