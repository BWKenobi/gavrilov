from django.conf import settings
from django import forms
from django.contrib.auth.models import User

from profileuser.clearablefileinput import CustomClearableFileInput, CustomClearableFileSimpleInput

from .models import Picture
from profileuser.models import CoProfile


class PictureUploadForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ('participation', 'author', 'ages', 'year', 'name', 'technique', 'nomination')

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field == 'participation':
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'disabled': 'disabled'})
			else:
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field in ['technique', 'participation']:
				self.fields[field].required=False
			else:
				self.fields[field].required=True

		self.fields['nomination'].empty_label = None


class PictureEditForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ('author', 'ages', 'year', 'name', 'technique', 'nomination')

		# widgets = {
		# 	'file': CustomClearableFileSimpleInput(),
		# 	'add_view_1': CustomClearableFileInput(),
		# 	'add_view_2': CustomClearableFileInput(),
		# }

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field in ['technique',]:
				self.fields[field].required=False
			else:
				self.fields[field].required=True

		self.fields['nomination'].empty_label = None

