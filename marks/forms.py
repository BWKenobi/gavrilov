from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import PictureMark, MasterMark


class PictureMarkForm(forms.ModelForm):
	class Meta:
		model = PictureMark
		fields = ('criterai_one', 'criterai_two', 'criterai_three', 'criterai_four', 'criterai_five')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'max': '10', 'min': '1'})
			self.fields[field].required=False


class MasterMarkForm(forms.ModelForm):
	class Meta:
		model = MasterMark
		fields = ('criterai_one', 'criterai_two', 'criterai_three', 'criterai_four', 'criterai_five')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false', 'max': '10', 'min': '1'})
			self.fields[field].required=False
