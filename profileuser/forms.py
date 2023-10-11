from django.conf import settings
from django import forms
from django.contrib.auth.models import User as UserModel
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


class UserRegistrationForm(forms.ModelForm):
	CHOICES = (
		('1', 'Студенты (профи) высших учебных заведений'),
		('2', 'Студенты (любители) высших учебных заведений'),
		('3', 'Студенты (профи) учреждений среднего профессионального образовани'),
		('4', 'Студенты (любители) учреждений среднего профессионального образовани'),
		('5', 'Профи'),
		('6', 'Любители'),
	)

	PROFILE_TYPE = (
		('0', 'участник'),
		('1', 'руководитель'),
		('2', 'преподаватель'),
		('3', 'хормейстер'),
		('4', 'концертмейстер'),
		('5', 'хореограф'),
	)

	email = forms.EmailField(label = 'E-mail*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	less_institution = forms.BooleanField(label = "Участие без представения учреждения", widget=forms.CheckboxInput(attrs={'class': 'form-controll', 'autocomplete':'false'}), required=False)
	category = forms.ChoiceField(choices=CHOICES, label = 'Категория*',  widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	surname = forms.CharField(label = 'Фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	profile_type = forms.ChoiceField(choices=PROFILE_TYPE, label='Должность*', widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	phone  = forms.CharField(label = 'Телефон*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	institution = forms.CharField(label = 'Полное назавние учреждения (в соответсие с ЕГЮРЛ)*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	institution_shot = forms.CharField(label = 'Сокращеное назавние учреждения*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	adress = forms.CharField(label = 'Адрес учреждения*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)

	add_team = forms.BooleanField(label = "Добавить коллектив", widget=forms.CheckboxInput(attrs={'class': 'form-controll', 'autocomplete':'false'}), required=False)
	team = forms.CharField(label = 'Название коллектива*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)


	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)


	class Meta:
		model = User
		fields = ('email',)


	def clean(self):
		data = self.cleaned_data
		email = data.get('email').lower()

		try:
			vaild_user = UserModel.objects.get(username=email)
		except UserModel.DoesNotExist:
			if email and UserModel.objects.filter(email=email).count()>0:
				raise forms.ValidationError('Используйте другой адрес электронной почты!')

			data['email'] = data['email'].lower()
			return data

		raise forms.ValidationError('Пользователь с таким email существует!')
