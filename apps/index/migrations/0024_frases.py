# Generated by Django 4.2.4 on 2023-11-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_alter_laudo_clinica_alter_laudo_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
