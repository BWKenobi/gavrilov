from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Child
from teachers.models import Teacher


class ChildForm(forms.ModelForm):
	class Meta:
		model = Child
		fields = ('surname', 'name', 'name2', 'age', 'group', 'master_flag', 'teacher_plus_flag', 'teacher_plus')

	def __init__(self, *args, **kwargs):
		admin = kwargs.pop('admin', None)
		super().__init__(*args, **kwargs)
		if admin:
			self.fields['teacher_plus'].queryset = Teacher.objects.filter(host_accaunt=admin.id)
		for field in self.fields:
			if field != 'teacher_plus_flag' and field != 'master_flag':
				self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if field != 'teacher_plus_flag' and field != 'teacher_plus' and field != 'master_flag':
				self.fields[field].required=True


class GroupForm(forms.ModelForm):
	class Meta:
		model = Child
		fields = ('group',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['group'].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})


class MasterUploadForm(forms.ModelForm):
	class Meta:
		model = Child
		fields = ('file_one', 'file_two', 'file_fin')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control autosubmition', 'autocomplete':'false'})
