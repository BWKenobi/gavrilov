import os
from pytils import translit

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from nominations.models import ArtNomination


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
	name = models.CharField(verbose_name="Название работы", max_length=100, blank=True)
	author = models.ForeignKey(User, verbose_name='Автор работы', on_delete=models.CASCADE)
	nomination = models.ForeignKey(ArtNomination, verbose_name='Номинация', on_delete=models.SET_NULL, blank=True, null=True, default=None)
	technique = models.CharField(verbose_name="Техника исполнения", max_length=50, blank=True)
	file = models.ImageField(verbose_name='Изображение работы', blank=True, null=True, upload_to = make_picture_path)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)


	class Meta:
		ordering = ['nomination', 'name']
		verbose_name='Работа'
		verbose_name_plural='Работы'


	def __str__(self):
		return self.name


######################################################################
@receiver(post_delete, sender = Picture)
def profile_post_delete_handler(sender, **kwargs):
	picture = kwargs['instance']

	if picture.file:
		if os.path.isfile(picture.file.path):
			os.remove(picture.file.path)


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
	