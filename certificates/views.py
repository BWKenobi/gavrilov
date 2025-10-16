import os
import io
import time
from datetime import date
import json
from io import BytesIO
import base64

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.sites.shortcuts import get_current_site

from pytils import translit

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from zipfile import ZipFile

from fpdf import FPDF

from profileuser.models import Profile, CoProfile
from movies.models import Movie, CoMovie


class PDF(FPDF):
	pass

@login_required(login_url='/login/')
def view_serificates(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	movies = Movie.objects.filter(has_come = True)

	coprofiles_pk = []
	for movie in movies:
		coprofiles_pk.append(movie.author.pk)
		comovies = CoMovie.objects.filter(movie = movie)
		for comovie in comovies:
			coprofiles_pk.append(comovie.coauthor.pk)

	coprofiles = CoProfile.objects.filter(pk__in = coprofiles_pk).order_by('main_user', 'surname', 'name','name2')

	args = {
		'coprofiles': coprofiles,
	}
	return render(request, 'certificates/view_serificates.html', args)


@login_required(login_url='/login/')
def view_my_serificates(request):
	coprofiles = CoProfile.objects.filter(main_user = request.user).order_by('surname', 'name','name2')

	args = {
		'coprofiles': coprofiles,
	}
	return render(request, 'certificates/view_my_serificates.html', args)


@login_required(login_url='/login/')
def del_serificates(request):
	coprofiles = CoProfile.objects.all()

	for coprofile in coprofiles:
		coprofile.certificate_file = None
		coprofile.save()

	return redirect('certificates:view_serificates')


@login_required(login_url='/login/')
def send_serificates(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	users_pk = list(Movie.objects.filter(has_come = True).values_list('author__main_user', flat=True))
	users = User.objects.filter(pk__in = users_pk)

	current_site = get_current_site(request)
	protocol = 'http'
	if request.is_secure():
		protocol = 'https'
	domain = current_site.domain

	count = 0
	for user in users:
		mail_subject = 'Информационное письмо'
		if settings.DEBUG:
			to_email = 'bwkenobi@yandex.ru'
		else:
			to_email = user.user.email

		sex = user.profile.sex()
		sex_valid = user.profile.sex_valid()
		name = user.profile.get_io_name()

		movies = Movie.objects.filter(author__main_user = user)

		coprofiles_pk = []
		for movie in movies:
			comovies = CoMovie.objects.filter(movie = movie)
			for comovie in comovies:
				coprofiles_pk.append(comovie.coauthor.pk)

		addons = CoProfile.objects.filter(pk__in = coprofiles_pk).order_by('surname', 'name','name2')

		coprofile = CoProfile.objects.filter(main_user=user, self_flag = True).first()
		args = {
			'sex_valid': sex_valid,
			'sex': sex, 
			'name': name,
			'addons': addons,
			'protocol': protocol,
			'domain': domain
		}
		
		message = render_to_string('certificates/info_email.html', args)

		message_html = render_to_string('certificates/info_email_html.html', args)

		email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

		email.attach_file(coprofile.certificate_file.path)
				
		email.send()

		count += 1

		if count==5:
			count = 0
			time.sleep(1.5)

	return redirect('certificates:view_serificates')


@login_required(login_url='/login/')
def generate_sertificates(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	movies = Movie.objects.filter(has_come = True)

	coprofiles_pk = []
	for movie in movies:
		coprofiles_pk.append(movie.author.pk)
		comovies = CoMovie.objects.filter(movie = movie)
		for comovie in comovies:
			coprofiles_pk.append(comovie.coauthor.pk)

	coprofiles = CoProfile.objects.filter(pk__in = coprofiles_pk).order_by('main_user', 'surname', 'name','name2')


	font_url = os.path.join(settings.BASE_DIR, 'static/fonts/chekhovskoy.ttf')
	img_url = os.path.join(settings.BASE_DIR, 'static/img/cer-2025.jpg')

	for coprofile in coprofiles:
		pdf = PDF(orientation='P', unit='mm', format='A4')
		pdf.add_page()
		pdf.add_font('Chehkovskoy', '', font_url , uni=True)
		pdf.image(img_url, 0, 0, pdf.w, pdf.h)
		
		pdf.set_font('Chehkovskoy', '', 18)
		pdf.set_text_color(0, 0, 0)
		pdf.set_xy(5.0, 180.0)
		if coprofile.profile_type == '0':
			pdf.multi_cell(w=200.0, h=5.0, align='C', txt = coprofile.get_full_name() + '\n\n' + coprofile.main_user.profile.institution)
		else:
			pdf.multi_cell(w=200.0, h=5.0, align='C', txt = coprofile.get_full_name() + ' (' + coprofile.get_profile_type_display() + ')\n\n' + coprofile.main_user.profile.institution)

		pdf.output(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), 'F')
		file  = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), 'rb')
		djangofile = File(file)

		coprofile.certificate_file.save(coprofile.get_full_name() + '.pdf', djangofile)
		coprofile.save()

		file.close()


	return HttpResponse('')

