# Generated by Django 2.2.24 on 2021-09-26 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artnomination',
            name='qwe',
        ),
        migrations.RemoveField(
            model_name='vocalnomination',
            name='qwe',
        ),
    ]