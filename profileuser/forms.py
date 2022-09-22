from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Profile, CoProfile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'group', 'institution', 'adress')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field == 'surname' or field == 'name':
				self.fields[field].required=True
			else:
				self.fields[field].required=False
			#self.fields[field].widget.attrs['disabled'] = 'disabled'


class CoProfileForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('surname', 'name', 'name2', 'profile_type')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field == 'surname' or field == 'name':
				self.fields[field].required=True
			else:
				self.fields[field].required=False
			#self.fields[field].widget.attrs['disabled'] = 'disabled'