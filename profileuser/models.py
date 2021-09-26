import os
from pytils import translit

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

def make_certificate_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'sertificate/%s' % new_filename

	return path


class Profile(models.Model):
	CATEGORY_TYPES = (
		('1', 'Студенты учреждений среднего профессионального образовани'),
		('2', 'Студенты высших учебных заведений'),
		('3', 'Преподаватели, руководители коллективов'),
		('4', 'Любительские коллективы'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
	username = models.CharField("Username:", max_length=30, blank=True)

	category  = models.CharField(verbose_name='Категория участника', max_length=1, choices=CATEGORY_TYPES, default='1')

	surname = models.CharField(verbose_name="Фамилия", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
	rank = models.TextField(verbose_name='Звания', blank=True)

	group = models.CharField(verbose_name="Название коллектива", max_length=250, blank=True)
	
	institution = models.CharField(verbose_name="Учреждение", max_length=250, blank=True)
	adress = models.CharField(verbose_name="Адрес учреждения", max_length=250, blank=True)

	surname_teacher = models.CharField(verbose_name="Фамилия преподавателя", max_length=50, blank=True)
	name_teacher = models.CharField(verbose_name="Имя преподавателя", max_length=30, blank=True)
	name2_teacher = models.CharField(verbose_name="Отчество преподавателя", max_length=30, blank=True)

	surname_musician = models.CharField(verbose_name="Фамилия концертмейстера", max_length=50, blank=True)
	name_musician = models.CharField(verbose_name="Имя концертмейстера", max_length=30, blank=True)
	name2_musician = models.CharField(verbose_name="Отчество концертмейстера", max_length=30, blank=True)

	certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)
	certificate_file = models.FileField(verbose_name='Сертификат', blank=True, null=True, upload_to = make_certificate_path)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)
	member_access= models.BooleanField("Права участника", default=True)
	admin_access= models.BooleanField("Права администратора", default=False)
	moderator_access= models.BooleanField("Права модератора", default=False)
	message_accecc = models.BooleanField("Права рассылки оповещений", default=False)

	juri_accecc = models.BooleanField("Член жюри", default=False)
	chef_juri_accecc = models.BooleanField("Председатель жюри", default=False)


	def __str__(self):
		if self.user.is_active:
			return self.get_file_name()
		return self.username + ' (not active)'


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


	def get_name(self):
		admin = ''
		if self.admin_access:
			admin = ' (Администратор)'
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.' + admin
			return self.surname + ' ' + self.name[0]+ '.'  + admin

		return self.name + admin


	def get_file_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.'
			return self.surname + ' ' + self.name[0]+ '.'

		if self.name:
			return self.name

		return str(self.user)
	


	def get_io_name(self):
		if self.name2:
			return self.name + ' ' + self.name2 
		return self.name 


	def get_full_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name + ' ' + self.name2 
			return self.surname + ' ' + self.name 

		return self.name

	#Имя файла без пути
	def file_short_name(self):
		str = self.report_file.path
		str = str[str.rfind('/')+1:len(str):1]
		return str


######################################################################
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.username = instance.username
	instance.profile.save()


@receiver(post_delete, sender = Profile)
def profile_post_delete_handler(sender, **kwargs):
	profile = kwargs['instance']

	if profile.certificate_file:
		if os.path.isfile(profile.certificate_file.path):
			os.remove(profile.certificate_file.path)


@receiver(pre_save, sender = Profile)
def profile_pre_save_handler(sender, **kwargs):
	profile = kwargs['instance']

	if not profile.pk:
		return False

	try:
		old_file = Profile.objects.get(pk=profile.pk).certificate_file

		if old_file:
			new_file = profile.certificate_file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Profile.DoesNotExist:
		pass
	