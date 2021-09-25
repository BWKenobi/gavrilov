import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from teachers.models import Teacher


def make_picture_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'master_pictures/%s' % new_filename

	return path


class Child(models.Model):
	GROUP = (
		('1', 'Студенты СПО'),
		('2', 'Студенты ВПО'),
		('3', 'ДШИ, ДХШ (13-14 лет)'),
		('4', 'ДШИ, ДХШ (от 15 лет)'),
	)

	surname = models.CharField(verbose_name="Фамилия участника", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя участника", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество участника", max_length=30, blank=True)
	age = models.DecimalField("Возраст участника", max_digits=2, decimal_places=0, blank=True, null=True, default=None)
	group = models.CharField(verbose_name="Возрастная группа", max_length=1, choices=GROUP, blank=True, null=True, default=None)	

	master_flag = models.BooleanField("Участие в конкурсе профессионального мастерства", default=False)


	teacher = models.ForeignKey(User, verbose_name='Преподаватель (Администратор)', on_delete=models.CASCADE)
	teacher_plus_flag = models.BooleanField("Другой преподаватель", default=False)
	teacher_plus = models.ForeignKey(Teacher, verbose_name='Преподаватель:', on_delete=models.SET_NULL, blank=True, null=True, default=None)

	file_one = models.ImageField(verbose_name='Изображение первого этапа', blank=True, null=True, upload_to = make_picture_path)
	file_two = models.ImageField(verbose_name='Изображение второго этапа', blank=True, null=True, upload_to = make_picture_path)
	file_fin = models.ImageField(verbose_name='Изображение законченной работы', blank=True, null=True, upload_to = make_picture_path)

	#certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)



	class Meta:
		ordering = ['surname', 'name', 'name2']
		verbose_name='Участник'
		verbose_name_plural='Участники'


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


	def get_file_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.'
			return self.surname + ' ' + self.name[0]+ '.'

		return self.name


	def sex(self):
		sex = False
		if self.name2[-1] =='ч' or self.name2[-1] == 'Ч':
			sex = True
		return sex


	def sex_valid(self):
		sex_valid = False
		if self.name2[-1] =='ч' or self.name2[-1] == 'Ч' or self.name2[-1] =='а' or self.name2[-1] == 'А':
			sex_valid = True
		return sex_valid


######################################################################
@receiver(post_delete, sender = Child)
def profile_post_delete_handler(sender, **kwargs):
	child = kwargs['instance']

	if child.file_one:
		if os.path.isfile(child.file_one.path):
			os.remove(child.file_one.path)

	if child.file_two:
		if os.path.isfile(child.file_two.path):
			os.remove(child.file_two.path)

	if child.file_fin:
		if os.path.isfile(child.file_fin.path):
			os.remove(child.file_fin.path)


@receiver(pre_save, sender = Child)
def profile_pre_save_handler(sender, **kwargs):
	child = kwargs['instance']

	if not child.pk:
		return False

	try:
		old_file = Child.objects.get(pk=child.pk).file_one

		if old_file:
			new_file = child.file_one
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Child.DoesNotExist:
		pass

	try:
		old_file = Child.objects.get(pk=child.pk).file_two

		if old_file:
			new_file = child.file_two
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Child.DoesNotExist:
		pass

	try:
		old_file = Child.objects.get(pk=child.pk).file_fin

		if old_file:
			new_file = child.file_fin
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Child.DoesNotExist:
		pass