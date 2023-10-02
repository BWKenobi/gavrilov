from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Profile, CoProfile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('category', 'surname', 'name', 'name2', 'phone', 'profile_type', 'less_institution', 'institution', 'institution_shot', 'adress')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			if field == 'less_institution':
				self.fields[field].widget.attrs.update({'autocomplete':'false'})
			else:
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field == 'surname' or field == 'name':
				self.fields[field].required=True
			else:
				self.fields[field].required=False


class CoProfileForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('surname', 'name', 'name2', 'profile_type')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		choices = self.fields['profile_type'].choices
		choices.pop(0)
		self.fields['profile_type'].choices = choices

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field == 'surname' or field == 'name':
				self.fields[field].required=True
			else:
				self.fields[field].required=False


class CoProfileTeamForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('coprofile_type', 'surname', 'name', 'name2', 'team',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False


class CoProfileTeamEditForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('coprofile_type', 'surname', 'name', 'name2', 'team',)

	def __init__(self, *args, **kwargs):
		admin_access = kwargs.pop('admin_access', None)
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False

		if not admin_access:
			self.fields['coprofile_type'].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'disabled': 'disabled'})
