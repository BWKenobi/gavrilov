from django.conf import settings
from django import forms
from django.contrib.auth.models import User

from profileuser.clearablefileinput import CustomClearableFileInput, CustomClearableFileSimpleInput

from .models import Picture
from profileuser.models import CoProfile


class PictureUploadForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ('participation', 'author', 'ages', 'year', 'name', 'technique', 'nomination', 'file', 'add_views', 'add_view_1', 'add_view_2')

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			if field == 'add_views':
				self.fields[field].widget.attrs.update({'autocomplete':'false'})
			else:
				if field == 'participation':
					self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'disabled': 'disabled'})
				else:
					self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field in ['file', 'add_view_1', 'add_view_2', 'technique', 'add_views', 'participation']:
				self.fields[field].required=False
			else:
				self.fields[field].required=True

		self.fields['nomination'].empty_label = None


class PictureEditForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ('author', 'ages', 'year', 'name', 'technique', 'nomination', 'file', 'add_views', 'add_view_1', 'add_view_2')

		widgets = {
			'file': CustomClearableFileSimpleInput(),
			'add_view_1': CustomClearableFileInput(),
			'add_view_2': CustomClearableFileInput(),
		}

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('author', None)
		super().__init__(*args, **kwargs)
		authors = CoProfile.objects.filter(main_user = user, profile_type = '0')
		self.fields['author'].queryset = authors
		self.fields['author'].empty_label = None

		for field in self.fields:
			if field == 'add_views':
				self.fields[field].widget.attrs.update({'autocomplete':'false'})
			else:
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})

			if field in ['file', 'add_view_1', 'add_view_2', 'technique', 'add_views']:
				self.fields[field].required=False
			else:
				self.fields[field].required=True

		self.fields['nomination'].empty_label = None

