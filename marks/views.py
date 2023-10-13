import os
import time
import operator

from django.db.models import Q
from datetime import date
import json
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User

from pytils import translit

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.shared import Mm, Pt

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from movies.models import Movie
from pictures.models import Picture
from profileuser.models import Profile
from .models import MovieMark, PictureMark

@login_required(login_url='/login/')
def mark_card(request):
	if not request.user.profile.juri_accecc:
		return redirect('home')

	pk = 0
	mark1 = 11
	mark2 = 11
	mark3 = 11

	plus = False


	if request.POST:
		if 'forward' in request.POST:
			pk = int(request.POST['pk']) + 1
			plus = True
		elif 'rewerse' in request.POST:
			pk = int(request.POST['pk']) - 1
			if pk<1:
				pk = 1
	else:
		pk = 1

	movies = Movie.objects.filter(author__profile__has_come = True, author__profile__participation = '1').order_by('scene_num')
	
	criteria1 = 'Сложность и трактовка музыкальных произведений'
	criteria2 = 'Интонационная выразительность'
	criteria3 = 'Артистизм'

	if movies:
		old_movie = movies[0]
		for movie in movies:
			if plus:
				if movie.scene_num >= pk:
					break
			else:
				if movie.scene_num == pk:
					break
				if movie.scene_num > pk:
					movie = old_dance
					break
				old_movie = movie

		marks = MovieMark.objects.filter(expert=request.user, work=movie)
		if marks:
			if marks[0].criterai_one:
				mark1 = marks[0].criterai_one
			if marks[0].criterai_two:
				mark2 = marks[0].criterai_two
			if marks[0].criterai_three:
				mark3 = marks[0].criterai_three

		pk = movie.scene_num

	else: 
		movie = None

	
	args = {
		'movie': movie,
		'pk': pk,
		'criteria1': criteria1,
		'criteria2': criteria2,
		'criteria3': criteria3,
		'mark1': mark1,
		'mark2': mark2,
		'mark3': mark3,
	}

	return render(request, 'marks/mark_card.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
def ajax_set_marks(request):
	pk = int(request.GET['pk'])
	mark1 = int(request.GET['mark1'])
	mark2 = int(request.GET['mark2'])
	mark3 = int(request.GET['mark3'])

	marks = MovieMark.objects.filter(expert=request.user, work=pk)
	if marks:
		marks[0].criterai_one = mark1
		marks[0].criterai_two = mark2
		marks[0].criterai_three = mark3
		marks[0].save()
	else:
		MovieMark.objects.create(expert=request.user, work=Movie.objects.get(pk=pk), criterai_one = mark1, criterai_two = mark2, criterai_three = mark3)
	return HttpResponse(True)


def ajax_set_pict_marks(request):
	pk = int(request.GET['pk'])
	mark1 = int(request.GET['mark1'])
	mark2 = int(request.GET['mark2'])
	mark3 = int(request.GET['mark3'])
	mark4 = int(request.GET['mark4'])
	mark5 = int(request.GET['mark5'])

	marks = PictureMark.objects.filter(expert=request.user, work=pk).last()

	PictureMark.objects.filter(expert=request.user, work=pk).exclude(pk = marks.pk).delete()

	if marks:
		marks.criterai_one = mark1
		marks.criterai_two = mark2
		marks.criterai_three = mark3
		marks.criterai_four = mark4
		marks.criterai_five = mark5
		marks.save()
	else:
		PictureMark.objects.create(
			expert=request.user,
			work = Picture.objects.get(pk=pk),
			criterai_one = mark1,
			criterai_two = mark2,
			criterai_three = mark3,
			criterai_four = mark4,
			criterai_five = mark5,
		)
	return HttpResponse(True)
