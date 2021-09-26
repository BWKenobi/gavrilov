from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'institution', 'adress', 'surname_teacher', 'name_teacher', 'name2_teacher', 'surname_musician', 'name_musician', 'name2_musician')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field == 'surname' or field == 'name':
				self.fields[field].required=True
			#self.fields[field].widget.attrs['disabled'] = 'disabled'

