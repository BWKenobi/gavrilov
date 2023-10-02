import os
from pytils import translit

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


class Profile(models.Model):
	CATEGORY_TYPES = (
		('1', 'Студенты (профи) высших учебных заведений'),
		('2', 'Студенты (любители) высших учебных заведений'),
		('3', 'Студенты (профи) учреждений среднего профессионального образовани'),
		('4', 'Студенты (любители) учреждений среднего профессионального образовани'),
		('5', 'Профи'),
		('6', 'Любители'),
	)

	PROFILE_TYPE = (
		('0', 'участник'),
		('1', 'руководитель'),
		('2', 'преподаватель'),
		('3', 'хормейстер'),
		('4', 'концертмейстер'),
		('5', 'хореограф'),
	)


	JURI_TYPE = (
		('1', 'Вокал'),
		('2', 'ДПИ'),
	)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
	username = models.CharField("Username:", max_length=30, blank=True)

	category = models.CharField(verbose_name='Категория участника', max_length=1, choices=CATEGORY_TYPES, default='1')

	surname = models.CharField(verbose_name="Фамилия", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
	phone = models.CharField(verbose_name="Телефон", max_length=30, blank=True)
	rank = models.TextField(verbose_name='Звания', blank=True)
	profile_type = models.CharField(verbose_name='Должность', max_length=1, choices=PROFILE_TYPE, default='0')

	institution = models.CharField(verbose_name="Полное назавние учреждения (в соответсие с ЕГЮРЛ)", max_length=250, blank=True)
	institution_shot = models.CharField(verbose_name="Сокращеное назавние учреждения", max_length=250, blank=True)
	adress = models.CharField(verbose_name="Адрес учреждения", max_length=250, blank=True)
	less_institution = models.BooleanField("Без учреждения", default=False)

	member_access= models.BooleanField("Права участника", default=True)
	admin_access= models.BooleanField("Права администратора", default=False)
	message_accecc = models.BooleanField("Права рассылки оповещений", default=False)
	juri_accecc = models.BooleanField("Член жюри", default=False)
	chef_juri_accecc = models.BooleanField("Председатель жюри", default=False)
	juri_type = models.CharField(verbose_name='Тип судейства', max_length=1, choices=JURI_TYPE, default='1')

	has_come= models.BooleanField("Факт прибытия", default=False)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)

	def __str__(self):
		if self.user.is_active:
			return self.get_file_name()
		return self.username + ' (not active)'


	def sex(self):
		sex = False
		if self.name2:
			if self.name2[-1] =='ч' or self.name2[-1] == 'Ч':
				sex = True
		return sex


	def sex_valid(self):
		sex_valid = False
		if self.name2:
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


	def get_institute(self):
		if self.less_institution:
			return 'Не представляет учреждение'

		return self.institution_shot


	def get_institute_full(self):
		if self.less_institution:
			return 'Не представляет учреждение'

		return self.institution


	def get_institute_zip(self):
		if self.less_institution:
			return self.get_file_name()

		return self.institution_shot


class CoProfile(models.Model):
	PROFILE_TYPE = (
		('0', 'участник'),
		('1', 'руководитель'),
		('2', 'преподаватель'),
		('3', 'хормейстер'),
		('4', 'концертмейстер'),
		('5', 'хореограф'),
	)

	COPROFILE_TYPE = (
		('1', 'участник'),
		('2', 'коллектив'),
	)
	
	main_user = models.ForeignKey(User, on_delete=models.CASCADE)
	self_flag = models.BooleanField("Признак себя", default=False)

	profile_type = models.CharField(verbose_name='Должность*', max_length=1, choices=PROFILE_TYPE, default='0')
	coprofile_type = models.CharField(verbose_name='участник/коллектив', max_length=1, choices=COPROFILE_TYPE, default='1')

	surname = models.CharField(verbose_name="Фамилия*", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя*", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество", max_length=30, blank=True)

	team = models.CharField(verbose_name="Название коллектива*", max_length=30, blank=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)

	def __str__(self):
		if self.profile_type == '0':
			if self.coprofile_type == '2':
				return self.team
			return self.get_file_name()

		return self.get_file_name() + ' (' + self.get_profile_type_display() + ')'


	def sex(self):
		sex = False
		if self.name2:
			if self.name2[-1] =='ч' or self.name2[-1] == 'Ч':
				sex = True
		return sex


	def sex_valid(self):
		sex_valid = False
		if self.name2:
			if self.name2[-1] =='ч' or self.name2[-1] == 'Ч' or self.name2[-1] =='а' or self.name2[-1] == 'А':
				sex_valid = True
		return sex_valid


	def get_name(self):
		if self.coprofile_type == '2':
			return self.team

		admin = ''
		if self.admin_access:
			admin = ' (Администратор)'
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.' + admin
			return self.surname + ' ' + self.name[0]+ '.'  + admin

		return self.name + admin


	def get_file_name(self):
		if self.coprofile_type == '2':
			return self.team

		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.'
			return self.surname + ' ' + self.name[0]+ '.'

		if self.name:
			return self.name

		return str(self.main_user)
	

	def get_io_name(self):
		if self.coprofile_type == '2':
			return self.team

		if self.name2:
			return self.name + ' ' + self.name2 
		return self.name 


	def get_full_name(self):
		if self.coprofile_type == '2':
			return self.team

		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name + ' ' + self.name2 
			return self.surname + ' ' + self.name 

		return self.name


	def short_profile_type(self):
		SHORT_PROFILE_TYPE = {
			'0': 'уч.',
			'1': 'рук.',
			'2': 'пед.',
			'3': 'хорм.',
			'4': 'конц.',
			'5': 'хоре.'
		}

		return SHORT_PROFILE_TYPE[self.profile_type]


######################################################################
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.username = instance.username
	instance.profile.save()


@receiver(pre_save, sender = Profile)
def profile_pre_save_handler(sender, **kwargs):
	profile = kwargs['instance']

	if not profile.pk:
		return False

	phone_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	if not profile.pk:
		return False

	if profile.phone:
		phone = profile.phone

		new_phone = ''
		for digit in phone:
			if digit in phone_digits:
				new_phone += digit

		if len(new_phone)<11:
			new_phone = '8' + new_phone

		if new_phone[0]!='8':
			new_phone = '8' + new_phone[1:]

		profile.phone = new_phone


@receiver(post_save, sender=Profile)
def save_post_profile(sender, **kwargs):
	profile = kwargs['instance']

	coprofile = CoProfile.objects.filter(main_user = profile.user, self_flag = True).first()
	if coprofile:
		coprofile.surname = profile.surname
		coprofile.name = profile.name
		coprofile.name2 = profile.name2
		coprofile.profile_type = profile.profile_type
		coprofile.self_flag = True
		coprofile.coprofile_type = '1'
		coprofile.save()
	else:
		CoProfile.objects.create(
			main_user = profile.user,
			surname = profile.surname,
			name = profile.name,
			name2 = profile.name2,
			profile_type = profile.profile_type,
			self_flag = True,
			coprofile_type = '1'
		)


