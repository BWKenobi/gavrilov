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


class MovieFilter(forms.Form):
    movies = forms.ChoiceField(label = 'Автор - работа')

    def __init__(self, *args, **kwargs):
        movies = kwargs.pop('movies', None)
        selected = kwargs.pop('selected', None)
        super(MovieFilter, self).__init__(*args, **kwargs)
        CHOICES = tuple()
        for movie in movies:
            CHOICES = CHOICES + ((str(movie.pk), movie.author.get_full_name() + ' - ' + movie.name_1 + ' / ' + movie.name_2),)

        self.fields['movies'].choices=CHOICES
        if selected:
            self.fields['movies'].initial = selected

        self.fields['movies'].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
