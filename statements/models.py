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

	path = 'statement/%s' % new_filename

	return path


class Statement(models.Model):
	file = models.FileField(verbose_name='Файл заявки', blank=True, null=True, upload_to = make_invoice_path)
	owner = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE, blank=True, null=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['owner']
		verbose_name='Заявление'
		verbose_name_plural='Заявления'


	def __str__(self):
		return str(self.owner)


######################################################################
@receiver(post_delete, sender = Statement)
def statement_post_delete_handler(sender, **kwargs):
	statement = kwargs['instance']

	if statement.file:
		if os.path.isfile(statement.file.path):
			os.remove(statement.file.path)


@receiver(pre_save, sender = Statement)
def statement_pre_save_handler(sender, **kwargs):
	statement = kwargs['instance']

	if not statement.pk:
		return False

	try:
		old_file = Statement.objects.get(pk=statement.pk).file

		if old_file:
			new_file = statement.file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Statement.DoesNotExist:
		pass
	