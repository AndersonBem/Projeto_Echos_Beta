# Generated by Django 4.2.4 on 2025-01-24 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0068_despesa_alter_laudo_hora_envio'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDespesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
