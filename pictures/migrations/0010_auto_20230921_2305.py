# Generated by Django 2.2.24 on 2023-09-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0009_auto_20230921_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='year',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Год исполнения работы*'),
        ),
    ]
