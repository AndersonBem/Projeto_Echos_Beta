# Generated by Django 4.2.4 on 2023-11-14 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_rename_email_tutor_laudo_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laudo',
            old_name='paciente',
            new_name='nome',
        ),
        migrations.AlterField(
            model_name='laudo',
            name='data',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
