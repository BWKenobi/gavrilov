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
	name = models.CharField(verbose_name="Название произведения", max_length=100, blank=True)
	author = models.ForeignKey(User, verbose_name='Исполнитель', on_delete=models.CASCADE)
	nomination = models.ForeignKey(VocalNomination, verbose_name='Номинация', on_delete=models.SET_NULL, blank=True, null=True, default=None)
	composer = models.CharField(verbose_name="Автор музыки", max_length=110, blank=True)
	poet = models.CharField(verbose_name="Автор слов", max_length=100, blank=True)
	descritpion = models.CharField(verbose_name="Описание", max_length=250, blank=True)
	file = models.URLField(verbose_name='Ссылка на файл', max_length=250, blank=True, null=True)

	youtube_flag = models.BooleanField("Признак YouTube", default=False)


	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['nomination', 'name']
		verbose_name='Песня'
		verbose_name_plural='Песни'


	def __str__(self):
		return self.name


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