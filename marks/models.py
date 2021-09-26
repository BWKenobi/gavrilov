from django.db import models

from django.contrib.auth.models import User
from pictures.models import Picture


class PictureMark(models.Model):
	criterai_one = models.DecimalField(verbose_name="Соответствие выбранной теме", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_two = models.DecimalField(verbose_name="Техническое воспроизведение", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_three = models.DecimalField(verbose_name="Авторское новаторство", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_four = models.DecimalField(verbose_name="Эстетика подачи работы", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_five = models.DecimalField(verbose_name="Визуальное восприятие", blank=True, decimal_places=0, default=None, max_digits=2, null=True)

	expert = models.ForeignKey(User, verbose_name='Член жюри', on_delete=models.CASCADE, blank=True, null=True)
	work = models.ForeignKey(Picture, verbose_name='Работа', on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ['work']
		verbose_name='Оценка работы'
		verbose_name_plural='Оценки работы'

	def __str__(self):
		return str(self.work) + ' (' + str(self.expert.profile) + ')'


class MasterMark(models.Model):
	criterai_one = models.DecimalField(verbose_name="Соответствие выбранной теме", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_two = models.DecimalField(verbose_name="Техническое воспроизведение", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_three = models.DecimalField(verbose_name="Авторское новаторство", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_four = models.DecimalField(verbose_name="Эстетика подачи работы", blank=True, decimal_places=0, default=None, max_digits=2, null=True)
	criterai_five = models.DecimalField(verbose_name="Визуальное восприятие", blank=True, decimal_places=0, default=None, max_digits=2, null=True)

	expert = models.ForeignKey(User, verbose_name='Член жюри', on_delete=models.CASCADE, blank=True, null=True)
#	work = models.ForeignKey(Child, verbose_name='Конкурсант', on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ['expert']
		verbose_name='Оценка проф.мастерства'
		verbose_name_plural='Оценки проф.мастерства'

	def __str__(self):
		return str(self.work) + ' (' + str(self.expert.profile) + ')'
