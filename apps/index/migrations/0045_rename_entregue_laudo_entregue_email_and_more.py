# Generated by Django 4.2.4 on 2024-01-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0044_alter_clinica_options_alter_racacanino_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laudo',
            old_name='entregue',
            new_name='entregue_email',
        ),
        migrations.AddField(
            model_name='laudo',
            name='entregue_whats',
            field=models.BooleanField(default=False),
        ),
    ]
