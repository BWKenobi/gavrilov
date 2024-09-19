import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from nominations.models import ArtNomination
from profileuser.models import CoProfile


def make_picture_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'pictures/%s' % new_filename

	return path
	

class Picture(models.Model):
	PARTICIPATION_TYPE = (
		('1', 'очное'),
		('2', 'заочное'),
	)

	name = models.CharField(verbose_name="Название работы*", max_length=100, blank=True)
	author = models.ForeignKey(CoProfile, verbose_name='Автор работы*', on_delete=models.CASCADE)
	nomination = models.ForeignKey(ArtNomination, verbose_name='Номинация*', on_delete=models.SET_NULL, blank=True, null=True, default=None)
	technique = models.CharField(verbose_name="Техника исполнения", max_length=50, blank=True)

	ages = models.DecimalField(verbose_name="Возраст на момент написания работы*", max_digits=2, decimal_places=0, default=0, blank=False)
	year = models.DecimalField(verbose_name="Год исполнения работы*", max_digits=4, decimal_places=0, default=0, blank=False)

	participation = models.CharField(verbose_name='Тип участия*', max_length=1, choices=PARTICIPATION_TYPE, default='2')

	file = models.ImageField(verbose_name='Изображение работы*', blank=True, null=True, upload_to = make_picture_path)
	add_views = models.BooleanField("Дополнительные ракурсы", default=False)
	add_view_1 = models.ImageField(verbose_name='Дополнительный вид', blank=True, null=True, upload_to = make_picture_path)
	add_view_2 = models.ImageField(verbose_name='Дополнительный вид', blank=True, null=True, upload_to = make_picture_path)

	place = models.DecimalField(verbose_name="Место", max_digits=1, decimal_places=0, default=None, blank=True, null=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['nomination', 'name']
		verbose_name='Работа'
		verbose_name_plural='Работы'


	def __str__(self):
		return self.name

	def ages_prefix(self):
		mod = self.ages % 10
		mod_plus = (self.ages // 10) % 10
		if mod_plus != 1:
			if mod == 0:
				return 'лет'
			elif mod == 1:
				return 'год'
			elif mod < 5:
				return 'года'
		return 'лет'

class CoPicturee(models.Model):
	picture = models.ForeignKey(Picture, verbose_name='Произведение', on_delete=models.CASCADE)
	coauthor = models.ForeignKey(CoProfile, verbose_name='Соисполнитель', on_delete=models.CASCADE)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)

	class Meta:
		ordering = ['picture', 'coauthor']
		verbose_name='Соисполнитель'
		verbose_name_plural='Соисполнители'


	def __str__(self):
		return str(self.picture) + ' - ' + str(self.coauthor)


######################################################################
@receiver(post_delete, sender = Picture)
def profile_post_delete_handler(sender, **kwargs):
	picture = kwargs['instance']

	if picture.file:
		if os.path.isfile(picture.file.path):
			os.remove(picture.file.path)

	if picture.add_view_1:
		if os.path.isfile(picture.add_view_1.path):
			os.remove(picture.add_view_1.path)

	if picture.add_view_2:
		if os.path.isfile(picture.add_view_2.path):
			os.remove(picture.add_view_2.path)


@receiver(pre_save, sender = Picture)
def profile_pre_save_handler(sender, **kwargs):
	picture = kwargs['instance']

	if not picture.pk:
		return False

	try:
		old_file = Picture.objects.get(pk=picture.pk).file

		if old_file:
			new_file = picture.file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Picture.DoesNotExist:
		pass
	
	try:
		old_file = Picture.objects.get(pk=picture.pk).add_view_1

		if old_file:
			new_file = picture.add_view_1
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Picture.DoesNotExist:
		pass

	try:
		old_file = Picture.objects.get(pk=picture.pk).add_view_2

		if old_file:
			new_file = picture.add_view_2
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Picture.DoesNotExist:
		pass
