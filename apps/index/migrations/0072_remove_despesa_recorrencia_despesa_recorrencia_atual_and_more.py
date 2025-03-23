# Generated by Django 4.2.4 on 2025-01-31 16:31

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0071_alter_despesa_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='despesa',
            name='recorrencia',
        ),
        migrations.AddField(
            model_name='despesa',
            name='recorrencia_atual',
            field=models.DecimalField(blank=True, decimal_places=0, default=Decimal('0'), max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name='despesa',
            name='recorrencia_total',
            field=models.DecimalField(blank=True, decimal_places=0, default=Decimal('0'), max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='hora_envio',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 1, 31, 23, 0, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
