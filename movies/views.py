import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import MovieUploadForm, MovieEditForm
from .models import Movie


@login_required(login_url='/login/')
def view_movies(request):
	movies = Movie.objects.filter(author=request.user)

	if request.method=='POST':
		return redirect('movies:load_movie')

	args = {
		'movies': movies,
	}
	return render(request, 'movies/view_movies.html', args)


@login_required(login_url='/login/')
def load_movie(request):
	if not request.user.profile.member_access:
		return redirect('home')

	author = request.user


	if request.method=='POST':
		form_movie = MovieUploadForm(request.POST, label_suffix='')

		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			url = new_movie.file.split('=')
			if len(url)>1:
				url = url[1].split('&')
				new_movie.file = 'https://www.youtube.com/embed/' + url[0]
			new_movie.save()	

			return redirect('movies:view_movies')

		args = {
			'form': form_movie,
		}
		return render(request, 'movies/load_movie.html', args)	
	
	form_movie = MovieUploadForm(label_suffix='')

	args = {
		'form': form_movie,
	}
	return render(request, 'movies/load_movie.html', args)


@login_required(login_url='/login/')
def edit_movie(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	movie = Movie.objects.get(pk=pk)
	author = request.user

	if movie.author != author:
		return redirect('home')

	if request.method=='POST':
		form_movie = MovieEditForm(request.POST, instance=movie, label_suffix='')

		if form_movie.is_valid():
			new_movie = form_movie.save(commit=False)
			new_movie.author = author
			new_movie.save()	

			return redirect('movies:view_movies')

		args = {
			'form': form_movie,
		}
		return render(request, 'movies/edit_movie.html', args)	
	
	form_movie = MovieEditForm(instance=movie, label_suffix='')

	args = {
		'form': form_movie,
		'movie': movie
	}
	return render(request, 'movies/edit_movie.html', args)

	
# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_movie(request):
	movie_pk = request.GET['movie']
	movie = Movie.objects.get(pk=movie_pk)

	if movie.author != request.user:
		return HttpResponse(False)

	movie.delete()

	return HttpResponse(True)