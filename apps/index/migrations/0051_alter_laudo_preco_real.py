# Generated by Django 4.2.4 on 2024-01-29 14:06

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0050_laudo_data_pagamento_laudo_forma_pagamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laudo',
            name='preco_real',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=8, null=True),
        ),
    ]
