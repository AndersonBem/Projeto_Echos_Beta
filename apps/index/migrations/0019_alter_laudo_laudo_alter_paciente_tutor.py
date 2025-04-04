# Generated by Django 4.2.4 on 2023-11-17 13:39

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0018_rename_nome_paciente_laudo_paciente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laudo',
            name='laudo',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tutor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pacientes', to='index.tutor'),
        ),
    ]
