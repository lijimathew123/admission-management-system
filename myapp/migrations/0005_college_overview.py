# Generated by Django 5.0.2 on 2024-02-12 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_college_admission_college_affiliation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='overview',
            field=models.TextField(default='course overview here', max_length=300),
        ),
    ]
