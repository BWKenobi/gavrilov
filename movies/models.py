import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from nominations.models import VocalNomination
from profileuser.models import CoProfile


class Movie(models.Model):
	PARTICIPATION_TYPE = (
		('1', 'очное'),
		('2', 'заочное'),
	)

	author = models.ForeignKey(CoProfile, verbose_name='Исполнитель*', on_delete=models.CASCADE)
	age = models.CharField(verbose_name="Дата рождения исполнителя*", max_length=30, blank=True)

	nomination = models.ForeignKey(VocalNomination, verbose_name='Номинация*', on_delete=models.SET_NULL, blank=True, null=True, default=None)

	participation = models.CharField(verbose_name='Тип участия*', max_length=1, choices=PARTICIPATION_TYPE, default='1')

	name_1 = models.CharField(verbose_name="Название первого произведения*", max_length=100, blank=True)
	region_1 = models.CharField(verbose_name="Регион", max_length=100, blank=True)
	composer_1 = models.CharField(verbose_name="Автор музыки", max_length=110, blank=True)
	poet_1 = models.CharField(verbose_name="Автор слов", max_length=100, blank=True)

	name_2 = models.CharField(verbose_name="Название второго произведения*", max_length=100, blank=True)
	region_2 = models.CharField(verbose_name="Регион", max_length=100, blank=True)
	composer_2 = models.CharField(verbose_name="Автор музыки", max_length=110, blank=True)
	poet_2 = models.CharField(verbose_name="Автор слов", max_length=100, blank=True)

	descritpion = models.CharField(verbose_name="Техничесие требования", max_length=250, blank=True)

	file_1 = models.URLField(verbose_name='Ссылка на файл', max_length=250, blank=True, null=True)
	file_2 = models.URLField(verbose_name='Ссылка на файл', max_length=250, blank=True, null=True)

	youtube_flag_1 = models.BooleanField("Признак YouTube", default=False)
	youtube_flag_2 = models.BooleanField("Признак YouTube", default=False)

	scene_num = models.DecimalField(verbose_name="Порядковый номер выступления", decimal_places=0, max_digits=3, null=True, default=None, blank=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['nomination', 'name_1', 'name_2']
		verbose_name='Песня'
		verbose_name_plural='Песни'


	def __str__(self):
		return self.name_1 + ' - ' +self.name_2


class CoMovie(models.Model):
	movie = models.ForeignKey(Movie, verbose_name='Произведение', on_delete=models.CASCADE)
	coauthor = models.ForeignKey(CoProfile, verbose_name='Соисполнитель', on_delete=models.CASCADE)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)

	class Meta:
		ordering = ['movie', 'coauthor']
		verbose_name='Соисполнитель'
		verbose_name_plural='Соисполнители'


	def __str__(self):
		return str(self.movie) + ' - ' + str(self.coauthor)
