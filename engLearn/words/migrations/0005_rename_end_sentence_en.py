# Generated by Django 5.0.7 on 2024-08-19 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_remove_sentence_word_sentence_word'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sentence',
            old_name='end',
            new_name='en',
        ),
    ]
