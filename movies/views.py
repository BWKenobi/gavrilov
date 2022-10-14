import os
import datetime
import json

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from .forms import MovieUploadForm, MovieUploadNoneFileForm, MovieEditForm
from .models import Movie, CoMovie
from profileuser.models import Profile, CoProfile


@login_required(login_url='/login/')
def view_movies(request):
	movies = Movie.objects.filter(author=request.user)
	comovies_list = {}


	if request.method=='POST':
		return redirect('movies:load_movie')

	for movie in movies:
		comovies_list[movie.pk] = CoMovie.objects.filter(movie = movie)

	args = {
		'movies': movies,
		'comovies_list': comovies_list
	}
	return render(request, 'movies/view_movies.html', args)


@login_required(login_url='/login/')
def load_movie(request):
	if not request.user.profile.member_access:
		return redirect('home')

	author = request.user
	coprofiles = CoProfile.objects.filter(main_user = author)

	if request.method=='POST':
		if author.profile.participation == '2':
			form_movie = MovieUploadForm(request.POST, label_suffix='')
		else:
			form_movie = MovieUploadNoneFileForm(request.POST, label_suffix='')

		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			
			if author.profile.participation == '2':
				if 'youtu' in new_movie.file:
					url = new_movie.file.split('=')
					if len(url)>1:
						url = url[1].split('&')
						new_movie.file = 'https://www.youtube.com/embed/' + url[0]
					else:
						url = new_movie.file.split('/')
						new_movie.file = 'https://www.youtube.com/embed/' + url[len(url)-1]
					new_movie.youtube_flag = True
				
			new_movie.save()	

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoMovie.objects.filter(movie = new_movie, coauthor = coprofile):
						CoMovie.objects.create(movie = new_movie, coauthor = coprofile)
				else:
					CoMovie.objects.filter(movie = new_movie, coauthor = coprofile).delete()


			return redirect('movies:view_movies')

		args = {
			'form': form_movie,
			'coprofiles': coprofiles,
			'author': author
		}
		return render(request, 'movies/load_movie.html', args)	
	
	if author.profile.participation == '2':
		form_movie = MovieUploadForm(label_suffix='')
	else:
		form_movie = MovieUploadNoneFileForm(label_suffix='')

	args = {
		'form': form_movie,
		'coprofiles': coprofiles,
		'author': author
	}
	return render(request, 'movies/load_movie.html', args)


@login_required(login_url='/login/')
def load_movie_admin(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	author = Profile.objects.get(pk = pk).user
	coprofiles = CoProfile.objects.filter(main_user = author)

	if request.method=='POST':
		if author.profile.participation == '2':
			form_movie = MovieUploadForm(request.POST, label_suffix='')
		else:
			form_movie = MovieUploadNoneFileForm(request.POST, label_suffix='')

		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			
			if author.profile.participation == '2':
				if 'youtu' in new_movie.file:
					url = new_movie.file.split('=')
					if len(url)>1:
						url = url[1].split('&')
						new_movie.file = 'https://www.youtube.com/embed/' + url[0]
					else:
						url = new_movie.file.split('/')
						new_movie.file = 'https://www.youtube.com/embed/' + url[len(url)-1]
					new_movie.youtube_flag = True
				
			new_movie.save()	

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoMovie.objects.filter(movie = new_movie, coauthor = coprofile):
						CoMovie.objects.create(movie = new_movie, coauthor = coprofile)
				else:
					CoMovie.objects.filter(movie = new_movie, coauthor = coprofile).delete()


			return redirect('view_contestant', pk =author.profile.pk)

		args = {
			'form': form_movie,
			'coprofiles': coprofiles,
			'author': author
		}
		return render(request, 'movies/load_movie.html', args)	
	
	if author.profile.participation == '2':
		form_movie = MovieUploadForm(label_suffix='')
	else:
		form_movie = MovieUploadNoneFileForm(label_suffix='')

	args = {
		'form': form_movie,
		'coprofiles': coprofiles,
		'author': author
	}
	return render(request, 'movies/load_movie.html', args)


@login_required(login_url='/login/')
def edit_movie(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	movie = Movie.objects.get(pk=pk)
	author = request.user
	comovies_list = {}

	if movie.author != author:
		return redirect('home')

	coprofiles = CoProfile.objects.filter(main_user = author)

	if request.method=='POST':
		form_movie = MovieEditForm(request.POST, instance=movie, label_suffix='')
		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			new_movie.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoMovie.objects.filter(movie = movie, coauthor = coprofile):
						CoMovie.objects.create(movie = movie, coauthor = coprofile)
				else:
					CoMovie.objects.filter(movie = movie, coauthor = coprofile).delete()

			return redirect('movies:view_movies')

		args = {
			'form': form_movie,
		}
		return render(request, 'movies/edit_movie.html', args)	
	
	form_movie = MovieEditForm(instance=movie, label_suffix='')
	comovies = list(CoMovie.objects.filter(movie = movie).values_list('coauthor', flat=True))
	for coprofile in coprofiles:
		comovies_list[coprofile.pk] = coprofile.pk in comovies


	args = {
		'form': form_movie,
		'movie': movie,
		'coprofiles': coprofiles,
		'comovies_list': comovies_list
	}
	return render(request, 'movies/edit_movie.html', args)


@login_required(login_url='/login/')
def edit_movie_admin(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')
		
	movie = Movie.objects.get(pk=pk)
	author = movie.author
	comovies_list = {}

	if movie.author != author:
		return redirect('home')

	coprofiles = CoProfile.objects.filter(main_user = author)

	if request.method=='POST':
		form_movie = MovieEditForm(request.POST, instance=movie, label_suffix='')
		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			new_movie.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoMovie.objects.filter(movie = movie, coauthor = coprofile):
						CoMovie.objects.create(movie = movie, coauthor = coprofile)
				else:
					CoMovie.objects.filter(movie = movie, coauthor = coprofile).delete()

			return redirect('view_contestant', pk =author.profile.pk)

		args = {
			'form': form_movie,
		}
		return render(request, 'movies/edit_movie.html', args)	
	
	form_movie = MovieEditForm(instance=movie, label_suffix='')
	comovies = list(CoMovie.objects.filter(movie = movie).values_list('coauthor', flat=True))
	for coprofile in coprofiles:
		comovies_list[coprofile.pk] = coprofile.pk in comovies


	args = {
		'form': form_movie,
		'movie': movie,
		'coprofiles': coprofiles,
		'comovies_list': comovies_list
	}
	return render(request, 'movies/edit_movie.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_movie(request):
	movie_pk = request.GET['movie']
	movie = Movie.objects.get(pk=movie_pk)

	if not request.user.profile.admin_access and movie.author != request.user:
		return HttpResponse(False)

	movie.delete()

	return HttpResponse(True)


@login_required(login_url='/login/')
def ajax_change_scene_movie(request):
	data_list = json.loads(request.GET['data_list'])


	
	for key, val in data_list.items():
		movie = Movie.objects.get(pk=key)
		movie.scene_num = int(val)
		movie.save()

	return HttpResponse(True)