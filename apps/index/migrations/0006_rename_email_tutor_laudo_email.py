# Generated by Django 4.2.4 on 2023-11-14 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_paciente_sexo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laudo',
            old_name='email_tutor',
            new_name='email',
        ),
    ]
