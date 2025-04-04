# Generated by Django 4.2.4 on 2024-01-24 11:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0045_rename_entregue_laudo_entregue_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='observacao',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='hora_envio',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 24, 1, 0, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
