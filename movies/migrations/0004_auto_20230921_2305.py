# Generated by Django 2.2.24 on 2023-09-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20230918_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='descritpion_1',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='descritpion_2',
        ),
        migrations.AddField(
            model_name='movie',
            name='descritpion',
            field=models.CharField(blank=True, max_length=250, verbose_name='Техничесие требования'),
        ),
        migrations.AddField(
            model_name='movie',
            name='region_1',
            field=models.CharField(blank=True, max_length=100, verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='movie',
            name='region_2',
            field=models.CharField(blank=True, max_length=100, verbose_name='Регион'),
        ),
    ]
