# Generated by Django 2.2.24 on 2021-09-26 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pictures.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nominations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Название работы')),
                ('technique', models.CharField(blank=True, max_length=50, verbose_name='Техника исполнения')),
                ('file', models.ImageField(blank=True, null=True, upload_to=pictures.models.make_picture_path, verbose_name='Изображение работы')),
                ('registration_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор работы')),
                ('nomination', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nominations.ArtNomination', verbose_name='Номинация')),
            ],
            options={
                'verbose_name': 'Работа',
                'verbose_name_plural': 'Работы',
                'ordering': ['nomination', 'name'],
            },
        ),
    ]