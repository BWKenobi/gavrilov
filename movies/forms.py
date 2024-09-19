from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Movie
from profileuser.models import CoProfile


class MovieUploadForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('participation', 'nomination', 'author', 'age', 'name_1', 'region_1', 'composer_1', 'poet_1',\
			'name_2', 'region_2', 'composer_2', 'poet_2', 'file_1', 'file_2')#, 'descritpion')

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			if field == 'participation':
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'disabled': 'disabled'})
			else:
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field in ['name_1', 'name_2', 'nomination']:
				self.fields[field].required=True
			else:
				self.fields[field].required=False

		self.fields['nomination'].empty_label = None



class MovieEditForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('nomination', 'author', 'age', 'name_1', 'region_1', 'composer_1', 'poet_1',\
			'name_2', 'region_2', 'composer_2', 'poet_2', 'file_1', 'file_2')#, 'descritpion')

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field in ['name_1', 'name_2', 'nomination']:
				self.fields[field].required=True
			else:
				self.fields[field].required=False

		self.fields['nomination'].empty_label = None
