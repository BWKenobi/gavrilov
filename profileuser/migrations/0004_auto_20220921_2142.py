# Generated by Django 2.2.24 on 2022-09-21 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profileuser', '0003_profile_participation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name2_musician',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name2_teacher',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name_musician',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name_teacher',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='surname_musician',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='surname_teacher',
        ),
    ]
