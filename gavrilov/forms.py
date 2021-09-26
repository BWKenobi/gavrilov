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
	email = forms.EmailField(label = 'Ваш e-mail*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	surname = forms.CharField(label = 'Ваша фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Ваше имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Ваше отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	
	institution = forms.CharField(label = 'Учреждение', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	adress = forms.CharField(label = 'Адрес учреждения', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)

	surname_teacher = forms.CharField(label = 'Фамилия преподавателя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	name_teacher = forms.CharField(label = 'Имя преподавателя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	name2_teacher	 = forms.CharField(label = 'Отчество преподавателя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)

	surname_musician = forms.CharField(label = 'Фамилия концертмейстера', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	name_musician = forms.CharField(label = 'Имя концертмейстера', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	name2_musician	 = forms.CharField(label = 'Отчество концертмейстера', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)

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
	juri = forms.ModelChoiceField(queryset = Profile.objects.none(), label='Выберите члена жюри')
	chef = forms.BooleanField(initial=False, required=False, label = 'Председатель жюри')

	def __init__(self, *args, **kwargs):
		pretendents = kwargs.pop('pretendents', None)
		super(SetJuriForm, self).__init__(*args, **kwargs)
		self.fields['juri'].queryset = pretendents
		self.fields['juri'].widget.attrs.update({'class': 'form-control'})



class ChangeJuriForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('chef_juri_accecc',)


class NewJuriForm(forms.ModelForm):
	email = forms.EmailField(label = 'E-mail члена жюри*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Имя члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	surname = forms.CharField(label = 'Фамилия члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	institution = forms.CharField(label = 'Учреждение члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	adress = forms.CharField(label = 'Адрес учреждения члена жюри*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	rank = forms.CharField(label = 'Регалии члена жюри*', widget=forms.Textarea	(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	chef_juri_accecc = forms.BooleanField(initial=False, required=False, label = 'Председатель жюри')

	def __init__(self, *args, **kwargs):
		super(NewJuriForm, self).__init__(*args, **kwargs)


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
