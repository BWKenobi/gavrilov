from django.db import models

from django.contrib.auth.models import User
from pictures.models import Picture
from movies.models import Movie


class PictureMark(models.Model):
	criterai_one = models.DecimalField(verbose_name="Соответствие названию, полнота раскрытия", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_two = models.DecimalField(verbose_name="Техническое воспроизведение", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_three = models.DecimalField(verbose_name="Авторское новаторство", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_four = models.DecimalField(verbose_name="Эстетика подачи работы", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_five = models.DecimalField(verbose_name="Визуальное восприятие", blank=True, decimal_places=0, default=None, max_digits=2, null=True)

	expert = models.ForeignKey(User, verbose_name='Член жюри', on_delete=models.CASCADE, blank=True, null=True)
	work = models.ForeignKey(Picture, verbose_name='Работа', on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ['work']
		verbose_name='Оценка работы (ДПИ)'
		verbose_name_plural='Оценки работы (ДПИ)'

	def __str__(self):
		return str(self.work) + ' (' + str(self.expert.profile) + ')'


class MovieMark(models.Model):
	criterai_one = models.DecimalField(verbose_name="Сложность и трактовка музыкальных произведений", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_two = models.DecimalField(verbose_name="Интонационная выразительность", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_three = models.DecimalField(verbose_name="Артистизм", blank=True, decimal_places=0, default=None, max_digits=2, null=True)

	expert = models.ForeignKey(User, verbose_name='Член жюри', on_delete=models.CASCADE, blank=True, null=True)
	work = models.ForeignKey(Movie, verbose_name='Работа', on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ['work']
		verbose_name='Оценка работы (Вокал)'
		verbose_name_plural='Оценки работы (Вокал)'

	def __str__(self):
		return str(self.work) + ' (' + str(self.expert.profile) + ')'
