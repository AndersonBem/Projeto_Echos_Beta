# Generated by Django 4.2.4 on 2025-01-24 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0070_rename_nome_tipodespesa_nome_despesa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.tipodespesa'),
        ),
    ]
