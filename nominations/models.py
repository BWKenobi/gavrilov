from django.db import models

class Nomination(models.Model):
	name = models.CharField("Техника исполнения", max_length=100, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name='Техника исполнения'
		verbose_name_plural='Техники исполнения'


	def __str__(self):
		return self.name


class SubNomination(models.Model):
	nomination = models.ForeignKey(Nomination, verbose_name='Техника исполнения', on_delete=models.CASCADE)
	name = models.CharField("Направление", max_length=100, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name='Направление техники исполнения'
		verbose_name_plural='Направления техники исполнения'


	def __str__(self):
		return self.name
