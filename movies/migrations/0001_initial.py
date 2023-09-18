# Generated by Django 2.2.24 on 2023-09-18 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nominations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Название произведения')),
                ('composer', models.CharField(blank=True, max_length=110, verbose_name='Автор музыки')),
                ('poet', models.CharField(blank=True, max_length=100, verbose_name='Автор слов')),
                ('descritpion', models.CharField(blank=True, max_length=250, verbose_name='Описание')),
                ('file', models.URLField(blank=True, max_length=250, null=True, verbose_name='Ссылка на файл')),
                ('youtube_flag', models.BooleanField(default=False, verbose_name='Признак YouTube')),
                ('scene_num', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=3, null=True, verbose_name='Порядковый номер выступления')),
                ('registration_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('nomination', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nominations.VocalNomination', verbose_name='Номинация')),
            ],
            options={
                'verbose_name': 'Песня',
                'verbose_name_plural': 'Песни',
                'ordering': ['nomination', 'name'],
            },
        ),
        migrations.CreateModel(
            name='CoMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('coauthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileuser.CoProfile', verbose_name='Соисполнитель')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Соисполнитель',
                'verbose_name_plural': 'Соисполнители',
                'ordering': ['movie', 'coauthor'],
            },
        ),
    ]
