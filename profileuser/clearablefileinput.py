from django.forms import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
	template_name = 'widgets/customclearablefileinput.html'


class CustomClearableFileSimpleInput(ClearableFileInput):
	template_name = 'widgets/customclearablefilesimpleinput.html'