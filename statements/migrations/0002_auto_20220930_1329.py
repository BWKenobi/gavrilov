# Generated by Django 2.2.24 on 2022-09-30 10:29

from django.db import migrations, models
import statements.models


class Migration(migrations.Migration):

    dependencies = [
        ('statements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=statements.models.make_invoice_path, verbose_name='Файл заявки'),
        ),
    ]
