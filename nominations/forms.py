from django.conf import settings
from django import forms
from django.contrib.auth.models import User



class PictureFilter(forms.Form):
    pictures = forms.ChoiceField(label = 'Автор - работа')

    def __init__(self, *args, **kwargs):
        pictures = kwargs.pop('pictures', None)
        selected = kwargs.pop('selected', None)
        super(PictureFilter, self).__init__(*args, **kwargs)
        CHOICES = tuple()
        for picture in pictures:
            CHOICES = CHOICES + ((str(picture.pk), picture.author.get_full_name() + ' - ' + picture.name),)

        self.fields['pictures'].choices=CHOICES
        if selected:
            self.fields['pictures'].initial = selected

        self.fields['pictures'].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
