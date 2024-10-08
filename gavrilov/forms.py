from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User as UserModel
from django.contrib.auth.models import User
	
from profileuser.models import Profile

User = get_user_model()


class UserLoginForm(forms.Form):
	email = forms.EmailField(label = 'E-Mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email').lower()
		password = self.cleaned_data.get('password')
		
		if email and password:
			vaild_user = User.objects.filter(username=email)

			if not vaild_user:
				raise forms.ValidationError('Пользователь не существует!')

			if not vaild_user[0].is_active:
				raise forms.ValidationError('Адрес электронной почты не подтвержден!')

			user = authenticate(username = email, password = password)

			if not user:
				raise forms.ValidationError('Неверный пароль!')

		return super(UserLoginForm, self).clean(*args, **kwargs)


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

	email = forms.EmailField(label = 'Ваш e-mail*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	less_institution = forms.BooleanField(label = "Участие без представления учреждения", widget=forms.CheckboxInput(attrs={'class': 'form-controll', 'autocomplete':'false'}), required=False)
	category = forms.ChoiceField(choices=CHOICES, label = 'Категория*',  widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	surname = forms.CharField(label = 'Ваша фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Ваше имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Ваше отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	profile_type = forms.ChoiceField(choices=PROFILE_TYPE, label='Должность*', widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	phone  = forms.CharField(label = 'Ваш телефон*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	institution = forms.CharField(label = 'Полное название учреждения (в соответствие с ЕГЮРЛ)*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	institution_shot = forms.CharField(label = 'Сокращенное название учреждения*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	adress = forms.CharField(label = 'Адрес учреждения*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)

	add_team = forms.BooleanField(label = "Добавить коллектив", widget=forms.CheckboxInput(attrs={'class': 'form-controll', 'autocomplete':'false'}), required=False)
	team = forms.CharField(label = 'Название коллектива*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)


	password = forms.CharField(label = 'Задайте пароль*', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

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


class ChangePasswordForm(forms.Form):
	oldpassword = forms.CharField(label = 'Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), required=True)
	newpassword1 = forms.CharField(label = 'Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), required=True)
	newpassword2 = forms.CharField(label = 'Новый пароль еще раз', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), required=True)

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username')
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		oldpass = self.cleaned_data['oldpassword']
		newpass1 = self.cleaned_data['newpassword1']
		newpass2 = self.cleaned_data['newpassword2']

		if oldpass and newpass1 and newpass2:
			user = authenticate(username = self.username, password = oldpass)
			if user is None:
				raise forms.ValidationError('Неверный пароль!')

			if newpass1 != newpass2:
				raise forms.ValidationError('Парли не совпали!')
		return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
	class Meta:
		model = User
		fields = ['email']

	def __init__(self, *args, **kwargs):
		super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].label = ''

	def clean(self):
		self.cleaned_data['email'] = self.cleaned_data['email'].lower()
		return self.cleaned_data


class CustomSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
		super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
		self.fields['new_password1'].label = 'Пароль'
		self.fields['new_password2'].label = 'Пароль еще раз'


	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')

		if password1 != password2:
			raise forms.ValidationError('Пароли не совпали!')
		return password2


class SetJuriForm(forms.Form):
	CHOICES = (
		('1', 'Вокал'),
		('2', 'ДПИ'),
	)

	juri = forms.ModelChoiceField(queryset = Profile.objects.none(), label='Выберите члена жюри')
	chef = forms.BooleanField(initial=False, required=False, label = 'Председатель жюри')
	juri_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label = 'Тип судейства')

	def __init__(self, *args, **kwargs):
		pretendents = kwargs.pop('pretendents', None)
		super(SetJuriForm, self).__init__(*args, **kwargs)
		self.fields['juri'].queryset = pretendents
		self.fields['juri'].widget.attrs.update({'class': 'form-control'})
		#self.fields['juri_type'].widget.attrs.update({'class': 'form-check-inline'})
		self.fields['juri_type'].initial='1'



class ChangeJuriForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'chef_juri_accecc', 'juri_type', 'rank')

	def __init__(self, *args, **kwargs):
		super(ChangeJuriForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			if field != 'chef_juri_accecc':
				self.fields[field].widget.attrs.update({'class': 'form-control'})



class NewJuriForm(forms.ModelForm):
	CHOICES = (
		('1', 'Вокал'),
		('2', 'ДПИ'),
	)

	email = forms.EmailField(label = 'E-mail члена жюри*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	surname = forms.CharField(label = 'Фамилия члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Имя члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество члена жюри', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	institution = forms.CharField(label = 'Учреждение члена жюри', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	adress = forms.CharField(label = 'Адрес учреждения члена жюри', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	rank = forms.CharField(label = 'Регалии члена жюри', widget=forms.Textarea	(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	chef_juri_accecc = forms.BooleanField(initial=False, required=False, label = 'Председатель жюри')
	juri_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label = 'Тип судейства')

	def __init__(self, *args, **kwargs):
		super(NewJuriForm, self).__init__(*args, **kwargs)
		self.fields['juri_type'].initial='1'

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
