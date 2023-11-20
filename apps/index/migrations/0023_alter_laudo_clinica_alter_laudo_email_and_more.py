# Generated by Django 4.2.4 on 2023-11-20 12:09

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0022_laudospadrao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laudo',
            name='clinica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinicas', to='index.clinica'),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='email_extra',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='idade',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='laudo',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='peso',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='raca',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='sexo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='suspeita',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='telefone_extra',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='laudo',
            name='veterinario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='index.veterinario'),
        ),
    ]
