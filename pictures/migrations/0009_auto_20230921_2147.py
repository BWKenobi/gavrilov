# Generated by Django 2.2.24 on 2023-09-21 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0008_auto_20230921_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='summa',
            new_name='year',
        ),
    ]
