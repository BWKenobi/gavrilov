# Generated by Django 2.2.24 on 2022-09-21 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import protocols.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=protocols.models.make_invoice_path, verbose_name='Файл протокола')),
                ('registration_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Протокол',
                'verbose_name_plural': 'Протоколы',
                'ordering': ['owner'],
            },
        ),
    ]