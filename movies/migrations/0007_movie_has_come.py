# Generated by Django 2.2.24 on 2023-10-11 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20231002_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='has_come',
            field=models.BooleanField(default=False, verbose_name='Факт прибытия'),
        ),
    ]
