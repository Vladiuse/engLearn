# Generated by Django 5.0.7 on 2024-07-29 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_sentence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='eng',
            new_name='en',
        ),
    ]
