import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User

from pictures.models import Picture
from movies.models import Movie
from .models import ArtNomination, VocalNomination
from marks.models import PictureMark, MovieMark
from marks.forms import PictureMarkForm, MovieMarkForm
from .forms import PictureFilter, MovieFilter


# Оценивание ДПИ ЗАОЧНО
@login_required(login_url='/login/')
def view_art_nomination(request, pk):
	if not request.user.profile.juri_accecc and not request.user.profile.chef_juri_accecc:
		return redirect('home')

	nomination = ArtNomination.objects.get(pk=pk)
	pictures = Picture.objects.filter(nomination=nomination, participation = '2')

	criterai1 = 'Соответствие названию, полнота раскрытия'
	criterai2 = 'Техническое воспроизведение'
	criterai3 = 'Авторское новаторство'
	criterai4 = 'Эстетика подачи работы'
	criterai5 = 'Визуальное восприятие'

	mark1_list = {}
	mark2_list = {}
	mark3_list = {}
	mark4_list = {}
	mark5_list = {}


	for picture in pictures:
		marks = PictureMark.objects.filter(expert=request.user, work=picture).first()
		mark1_list[picture.pk] = None
		mark2_list[picture.pk] = None
		mark3_list[picture.pk] = None
		mark4_list[picture.pk] = None
		mark5_list[picture.pk] = None

		if marks:
			if marks.criterai_one:
				mark1_list[picture.pk] = marks.criterai_one
			if marks.criterai_two:
				mark2_list[picture.pk] = marks.criterai_two
			if marks.criterai_three:
				mark3_list[picture.pk] = marks.criterai_three
			if marks.criterai_four:
				mark4_list[picture.pk] = marks.criterai_four
			if marks.criterai_five:
				mark5_list[picture.pk] = marks.criterai_five


	args = {
		'nomination': nomination, 
		'pictures': pictures,
		'nomination_pk': pk,
		'criterai1': criterai1,
		'criterai2': criterai2,
		'criterai3': criterai3,
		'criterai4': criterai4,
		'criterai5': criterai5,
		'mark1_list': mark1_list,
		'mark2_list': mark2_list,
		'mark3_list': mark3_list,
		'mark4_list': mark4_list,
		'mark5_list': mark5_list,
	}
	return render(request, 'nominations/view_art_nominations.html', args)


# Оценивание ДПИ ОЧНО Админом
@login_required(login_url='/login/')
def view_art_far_nomination(request, pk = None):
	if not request.user.profile.admin_access:
		return redirect('home')

	pictures = Picture.objects.filter(participation = '1').order_by('author__surname', 'author__name', 'author__team')
	if not pk:
		if pictures.first():
			pk = pictures.first().pk


	form = PictureFilter(pictures = pictures, selected = str(pk))

	picture = Picture.objects.filter(pk = pk).first()

	users = User.objects.filter(profile__juri_accecc = True, profile__juri_type = '2')

	criterai1 = 'Соответствие названию, полнота раскрытия'
	criterai2 = 'Техническое воспроизведение'
	criterai3 = 'Авторское новаторство'
	criterai4 = 'Эстетика подачи работы'
	criterai5 = 'Визуальное восприятие'

	mark_container = {}

	for user in users:
		marks = PictureMark.objects.filter(expert=user, work=picture).first()
		mark1 = None
		mark2 = None
		mark3 = None
		mark4 = None
		mark5 = None

		if marks:
			if marks.criterai_one:
				mark1 = marks.criterai_one
			if marks.criterai_two:
				mark2 = marks.criterai_two
			if marks.criterai_three:
				mark3 = marks.criterai_three
			if marks.criterai_four:
				mark4 = marks.criterai_four
			if marks.criterai_five:
				mark5 = marks.criterai_five

		mark_container[user.pk] = {
			'mark1': mark1,
			'mark2': mark2,
			'mark3': mark3,
			'mark4': mark4,
			'mark5': mark5
		}

	print(mark_container)
	args = {
		'form': form,
		'pk': pk,
		'picture': picture,
		'users': users,
		'mark_container': mark_container,
		'criterai1': criterai1,
		'criterai2': criterai2,
		'criterai3': criterai3,
		'criterai4': criterai4,
		'criterai5': criterai5,
	}
	return render(request, 'nominations/view_art_far_nomination.html', args)



# Оценивание ВОКАЛ ЗАОЧНО
@login_required(login_url='/login/')
def view_movie_nomination(request, pk):
	if not request.user.profile.juri_accecc and not request.user.profile.chef_juri_accecc:
		return redirect('home')

	nomination = VocalNomination.objects.get(pk=pk)
	movies = Movie.objects.filter(nomination=nomination, participation = '2')

	criterai1 = 'Соответствие названию, полнота раскрытия'
	criterai2 = 'Техническое воспроизведение'
	criterai3 = 'Авторское новаторство'

	mark1_list = {}
	mark2_list = {}
	mark3_list = {}


	for movie in movies:
		marks = MovieMark.objects.filter(expert=request.user, work=movie).first()
		mark1_list[movie.pk] = None
		mark2_list[movie.pk] = None
		mark3_list[movie.pk] = None

		if marks:
			if marks.criterai_one:
				mark1_list[movie.pk] = marks.criterai_one
			if marks.criterai_two:
				mark2_list[movie.pk] = marks.criterai_two
			if marks.criterai_three:
				mark3_list[movie.pk] = marks.criterai_three



	args = {
		'nomination': nomination,
		'movies': movies,
		'nomination_pk': pk,
		'criterai1': criterai1,
		'criterai2': criterai2,
		'criterai3': criterai3,
		'mark1_list': mark1_list,
		'mark2_list': mark2_list,
		'mark3_list': mark3_list,
	}
	return render(request, 'nominations/view_movie_nominations.html', args)



# Оценивание ВОКАЛ ЗАОЧНО Админом
@login_required(login_url='/login/')
def view_movie_far_nomination(request, pk = None):
	if not request.user.profile.admin_access:
		return redirect('home')

	movies = Movie.objects.filter(participation = '2').order_by('author__surname', 'author__name', 'author__team')
	if not pk:
		pk = movies.first().pk


	form = MovieFilter(movies = movies, selected = str(pk))

	movie = Movie.objects.get(pk = pk)

	users = User.objects.filter(profile__juri_accecc = True, profile__juri_type = '1')

	criterai1 = 'Сложность и трактовка'
	criterai2 = 'Интонационная выразительность'
	criterai3 = 'Артистизм'

	mark_container = {}

	for user in users:
		marks = MovieMark.objects.filter(expert=user, work=movie).first()
		mark1 = None
		mark2 = None
		mark3 = None


		if marks:
			if marks.criterai_one:
				mark1 = marks.criterai_one
			if marks.criterai_two:
				mark2 = marks.criterai_two
			if marks.criterai_three:
				mark3 = marks.criterai_three

		mark_container[user.pk] = {
			'mark1': mark1,
			'mark2': mark2,
			'mark3': mark3,
		}

	print(mark_container)
	args = {
		'form': form,
		'pk': pk,
		'movie': movie,
		'users': users,
		'mark_container': mark_container,
		'criterai1': criterai1,
		'criterai2': criterai2,
		'criterai3': criterai3,
	}
	return render(request, 'nominations/view_movie_far_nomination.html', args)
