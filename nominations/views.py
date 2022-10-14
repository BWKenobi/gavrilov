import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from pictures.models import Picture
from movies.models import Movie
from .models import ArtNomination, VocalNomination
from marks.models import PictureMark, MovieMark
from marks.forms import PictureMarkForm, MovieMarkForm


@login_required(login_url='/login/')
def view_art_nomination(request, pk, tp = None):
	if not request.user.profile.juri_accecc and not request.user.profile.chef_juri_accecc:
		return redirect('home')

	nomination = ArtNomination.objects.get(pk=pk)
	if tp:
		pictures = Picture.objects.filter(nomination=nomination, author__profile__participation = '1')
	else:
		pictures = Picture.objects.filter(nomination=nomination, author__profile__participation = '2')

	if request.POST:
		criterai_one = request.POST.getlist('criterai_one')
		criterai_two = request.POST.getlist('criterai_two')
		criterai_three = request.POST.getlist('criterai_three')
		criterai_four = request.POST.getlist('criterai_four')
		criterai_five = request.POST.getlist('criterai_five')

		cnt = 0
		for picture in pictures:
			marks = PictureMark.objects.filter(expert=request.user, work=picture)
			if marks:
				mark = marks[0]

				if not criterai_one[cnt] and not criterai_two[cnt] and not criterai_three[cnt] and not criterai_four[cnt]\
					and not criterai_five[cnt]:
					mark.delete()
				else:
					if criterai_one[cnt]:
						mark.criterai_one = int(criterai_one[cnt])
						if mark.criterai_one>10:
							mark.criterai_one = 10
					else:
						mark.criterai_one = 0

					if criterai_two[cnt]:
						mark.criterai_two = int(criterai_two[cnt])
						if mark.criterai_two>10:
							mark.criterai_two = 10
					else:
						mark.criterai_two = 0

					if criterai_three[cnt]:
						mark.criterai_three = int(criterai_three[cnt])
						if mark.criterai_three>10:
							mark.criterai_three = 10
					else:
						mark.criterai_three = 0

					if criterai_four[cnt]:
						mark.criterai_four = int(criterai_four[cnt])
						if mark.criterai_four>10:
							mark.criterai_four = 10
					else:
						mark.criterai_four = 0

					if criterai_five[cnt]:
						mark.criterai_five = int(criterai_five[cnt])
						if mark.criterai_five>10:
							mark.criterai_five = 10
					else:
						mark.criterai_five = 0

					mark.save()
			else:
				if  criterai_one[cnt] or  criterai_two[cnt] or  criterai_three[cnt] or  criterai_four[cnt]\
					or  criterai_five[cnt]:
					mark = PictureMark.objects.create(expert = request.user, work = picture)

					if criterai_one[cnt]:
						mark.criterai_one = int(criterai_one[cnt])
						if mark.criterai_one>10:
							mark.criterai_one = 10
					else:
						mark.criterai_one = 0

					if criterai_two[cnt]:
						mark.criterai_two = int(criterai_two[cnt])
						if mark.criterai_two>10:
							mark.criterai_two = 10
					else:
						mark.criterai_two = 0

					if criterai_three[cnt]:
						mark.criterai_three = int(criterai_three[cnt])
						if mark.criterai_three>10:
							mark.criterai_three = 10
					else:
						mark.criterai_three = 0

					if criterai_four[cnt]:
						mark.criterai_four = int(criterai_four[cnt])
						if mark.criterai_four>10:
							mark.criterai_four = 10
					else:
						mark.criterai_four = 0

					if criterai_five[cnt]:
						mark.criterai_five = int(criterai_five[cnt])
						if mark.criterai_five>10:
							mark.criterai_five = 10
					else:
						mark.criterai_five = 0

					mark.save()

			cnt += 1


	forms = {}
	for picture in pictures:
		mark = PictureMark.objects.filter(expert=request.user, work=picture)
		if mark:
			form = PictureMarkForm(instance=mark[0], label_suffix='')
		else:
			form = PictureMarkForm(label_suffix='')

		forms[picture.id] = form

	args = {
		'nomination': nomination, 
		'pictures': pictures,
		'nomination_pk': pk,
		'forms': forms,
		'tp': tp
	}
	return render(request, 'nominations/view_art_nominations.html', args)


@login_required(login_url='/login/')
def view_movie_nomination(request, pk):
	if not request.user.profile.juri_accecc and not request.user.profile.chef_juri_accecc:
		return redirect('home')

	nomination = VocalNomination.objects.get(pk=pk)
	movies = Movie.objects.filter(nomination=nomination, author__profile__participation = '2')

	if request.POST:
		criterai_one = request.POST.getlist('criterai_one')
		criterai_two = request.POST.getlist('criterai_two')
		criterai_three = request.POST.getlist('criterai_three')

		cnt = 0
		for movie in movies:
			marks = MovieMark.objects.filter(expert=request.user, work=movie)
			if marks:
				mark = marks[0]

				if not criterai_one[cnt] and not criterai_two[cnt] and not criterai_three[cnt]:
					mark.delete()
				else:
					if criterai_one[cnt]:
						mark.criterai_one = int(criterai_one[cnt])
						if mark.criterai_one>10:
							mark.criterai_one = 10
					else:
						mark.criterai_one = 0

					if criterai_two[cnt]:
						mark.criterai_two = int(criterai_two[cnt])
						if mark.criterai_two>10:
							mark.criterai_two = 10
					else:
						mark.criterai_two = 0

					if criterai_three[cnt]:
						mark.criterai_three = int(criterai_three[cnt])
						if mark.criterai_three>10:
							mark.criterai_three = 10
					else:
						mark.criterai_three = 0

					mark.save()
			else:
				if  criterai_one[cnt] or  criterai_two[cnt] or  criterai_three[cnt]:
					mark = MovieMark.objects.create(expert = request.user, work = movie)

					if criterai_one[cnt]:
						mark.criterai_one = int(criterai_one[cnt])
						if mark.criterai_one>10:
							mark.criterai_one = 10
					else:
						mark.criterai_one = 0

					if criterai_two[cnt]:
						mark.criterai_two = int(criterai_two[cnt])
						if mark.criterai_two>10:
							mark.criterai_two = 10
					else:
						mark.criterai_two = 0

					if criterai_three[cnt]:
						mark.criterai_three = int(criterai_three[cnt])
						if mark.criterai_three>10:
							mark.criterai_three = 10
					else:
						mark.criterai_three = 0

					mark.save()

			cnt += 1


	forms = {}
	for movie in movies:
		mark = MovieMark.objects.filter(expert=request.user, work=movie)
		if mark:
			form = MovieMarkForm(instance=mark[0], label_suffix='')
		else:
			form = MovieMarkForm(label_suffix='')

		forms[movie.id] = form

	args = {
		'nomination': nomination, 
		'movies': movies,
		'nomination_pk': pk,
		'forms': forms
	}
	return render(request, 'nominations/view_movie_nominations.html', args)

