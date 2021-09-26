import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver



def make_certificate_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'certificates/%s' % new_filename

	return path


class Certificate(models.Model):
	TYPE = (
		('1', 'Диплом лауреата'),
		('2', 'Диплом учасника'),
		('3', 'Благодарственное письмо'),
		('4', 'Сертификат'),
	)

	contestant = models.ForeignKey(User, verbose_name='Конкурсант', on_delete=models.CASCADE, blank=True, null=True)

	type = models.CharField(verbose_name="Тип", max_length=1, choices=TYPE, default='4')	

	certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)
	certificate_file = models.FileField(verbose_name='Сертификат', blank=True, null=True, upload_to = make_certificate_path)

	registration_date = models.DateField(verbose_name="Дата создания", default=timezone.now)



	class Meta:
		ordering = ['type', 'certificate_num']
		verbose_name='Сертификат'
		verbose_name_plural='Сертификаты'


	def __str__(self):
		return self.get_type_display() + ' №' + self.certificate_num


######################################################################
@receiver(post_delete, sender = Certificate)
def profile_post_delete_handler(sender, **kwargs):
	sertificate = kwargs['instance']

	if sertificate.certificate_file:
		if os.path.isfile(sertificate.certificate_file.path):
			os.remove(sertificate.certificate_file.path)


@receiver(pre_save, sender = Certificate)
def profile_pre_save_handler(sender, **kwargs):
	sertificate = kwargs['instance']

	if not sertificate.pk:
		return False

	try:
		old_file = Certificate.objects.get(pk=sertificate.pk).certificate_file

		if old_file:
			new_file = sertificate.certificate_file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Certificate.DoesNotExist:
		pass
	
	