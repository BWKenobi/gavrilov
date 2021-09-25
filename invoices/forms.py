from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Invoice



class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = ('date', 'summa', 'file')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True