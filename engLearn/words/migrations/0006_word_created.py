# Generated by Django 5.0.7 on 2024-08-20 19:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0005_rename_end_sentence_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='created',
            field=models.DateField(auto_created=True, default=datetime.datetime(2024, 5, 12, 19, 40, 34, 372964, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
