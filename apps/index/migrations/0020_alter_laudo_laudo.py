# Generated by Django 4.2.4 on 2023-11-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0019_alter_laudo_laudo_alter_paciente_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laudo',
            name='laudo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
