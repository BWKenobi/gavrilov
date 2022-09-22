import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


def make_invoice_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'invoces/%s' % new_filename

	return path


class Invoice(models.Model):
	summa = models.DecimalField(verbose_name="Сумма оплаты", max_digits=7, decimal_places=2, default=0, blank=False)
	date = models.DateField(verbose_name="Дата оплаты", default=timezone.now)
	file = models.FileField(verbose_name='Файл квитанции', blank=True, null=True, upload_to = make_invoice_path)
	payer = models.ForeignKey(User, verbose_name='Плательщик', on_delete=models.CASCADE, blank=True, null=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['payer']
		verbose_name='Квитанция'
		verbose_name_plural='Квитанции'


	def __str__(self):
		return str(self.payer) + ' (' + str(self.summa) + ')'


######################################################################
@receiver(post_delete, sender = Invoice)
def invoice_post_delete_handler(sender, **kwargs):
	invoce = kwargs['instance']

	if invoce.file:
		if os.path.isfile(invoce.file.path):
			os.remove(invoce.file.path)


@receiver(pre_save, sender = Invoice)
def invoice_pre_save_handler(sender, **kwargs):
	invoce = kwargs['instance']

	if not invoce.pk:
		return False

	try:
		old_file = Invoice.objects.get(pk=invoce.pk).file

		if old_file:
			new_file = invoce.file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Invoice.DoesNotExist:
		pass
	