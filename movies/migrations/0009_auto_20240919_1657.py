# Generated by Django 2.2.24 on 2024-09-19 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_movie_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='participation',
            field=models.CharField(choices=[('1', 'очное'), ('2', 'заочное')], default='2', max_length=1, verbose_name='Тип участия*'),
        ),
    ]
