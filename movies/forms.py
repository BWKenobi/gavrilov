from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Movie


class MovieUploadForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('name', 'nomination', 'composer', 'poet', 'descritpion', 'file')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field=='name' or field=='nomination' or field=='file':
				self.fields[field].required=True
			else:
				self.fields[field].required=False


class MovieUploadNoneFileForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('name', 'nomination', 'composer', 'poet', 'descritpion')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field=='name' or field=='nomination':
				self.fields[field].required=True
			else:
				self.fields[field].required=False


class MovieEditForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ('name', 'nomination', 'composer', 'poet', 'descritpion')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field=='name' or field=='nomination' or field=='file':
				self.fields[field].required=True
			else:
				self.fields[field].required=False

