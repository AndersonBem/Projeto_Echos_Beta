# Generated by Django 4.2.4 on 2023-11-17 17:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0021_alter_laudo_laudo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaudosPadrao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_exame', models.CharField(max_length=100)),
                ('tipo_exame', models.CharField(max_length=100)),
                ('laudo', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
    ]
