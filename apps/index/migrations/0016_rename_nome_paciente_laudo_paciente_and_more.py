# Generated by Django 4.2.4 on 2023-11-16 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_rename_paciente_laudo_nome_paciente_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laudo',
            old_name='nome_paciente',
            new_name='paciente',
        ),
        migrations.RenameField(
            model_name='laudo',
            old_name='nome_tutor',
            new_name='tutor',
        ),
        migrations.RenameField(
            model_name='paciente',
            old_name='nome_paciente',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='paciente',
            old_name='nome_tutor',
            new_name='tutor',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='nome_tutor',
            new_name='nome',
        ),
    ]
