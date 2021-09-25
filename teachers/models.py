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

	path = 'reports/sertificate/%s' % new_filename

	return path


class Teacher(models.Model):
	surname = models.CharField(verbose_name="Фамилия преподавателя", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя преподавателя", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество преподавателя", max_length=30, blank=True)

	host_accaunt = models.ForeignKey(User, verbose_name='Администратор учреждения:', on_delete=models.CASCADE)


	certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)
	certificate_file = models.FileField(verbose_name='Сертификат', blank=True, null=True, upload_to = make_certificate_path)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['surname', 'name', 'name2']
		verbose_name='Преподаватель'
		verbose_name_plural='Преподаватели'


	def __str__(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.'
			return self.surname + ' ' + self.name[0]+ '.'

		return self.name

	def get_full_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name + ' ' + self.name2
			return self.surname + ' ' + self.name

		return self.name


######################################################################
@receiver(post_delete, sender = Teacher)
def profile_post_delete_handler(sender, **kwargs):
	teacher = kwargs['instance']

	if teacher.certificate_file:
		if os.path.isfile(teacher.certificate_file.path):
			os.remove(teacher.certificate_file.path)


@receiver(pre_save, sender = Teacher)
def profile_pre_save_handler(sender, **kwargs):
	teacher = kwargs['instance']

	if not teacher.pk:
		return False

	try:
		old_file = Teacher.objects.get(pk=teacher.pk).certificate_file

		if old_file:
			new_file = teacher.certificate_file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Teacher.DoesNotExist:
		pass
	