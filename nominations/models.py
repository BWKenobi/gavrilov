from django.db import models

class ArtNomination(models.Model):
	name = models.CharField("Номинация (ДПИ)", max_length=100, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name='Номинация (ДПИ)'
		verbose_name_plural='Номинации (ДПИ)'


	def __str__(self):
		return self.name


class VocalNomination(models.Model):
	name = models.CharField("Номинация (Вокал)", max_length=100, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name='Номинация (Вокал)'
		verbose_name_plural='Номинации (Вокал)'


	def __str__(self):
		return self.name