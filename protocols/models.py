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

	path = 'protocols/%s' % new_filename

	return path


class Protocol(models.Model):
	file = models.FileField(verbose_name='Файл протокола', blank=True, null=True, upload_to = make_invoice_path)
	owner = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE, blank=True, null=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['owner']
		verbose_name='Протокол'
		verbose_name_plural='Протоколы'


	def __str__(self):
		return str(self.owner)


######################################################################
@receiver(post_delete, sender = Protocol)
def protocol_post_delete_handler(sender, **kwargs):
	protocol = kwargs['instance']

	if protocol.file:
		if os.path.isfile(protocol.file.path):
			os.remove(protocol.file.path)


@receiver(pre_save, sender = Protocol)
def protocol_pre_save_handler(sender, **kwargs):
	protocol = kwargs['instance']

	if not protocol.pk:
		return False

	try:
		old_file = Protocol.objects.get(pk=protocol.pk).file

		if old_file:
			new_file = protocol.file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Protocol.DoesNotExist:
		pass
	