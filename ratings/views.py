import os
import datetime
import operator

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from pytils import translit

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.shared import Mm, Pt

from pictures.models import Picture
from movies.models import Movie
from nominations.models import ArtNomination, VocalNomination
from marks.models import PictureMark, MovieMark

from marks.forms import PictureMarkForm, MovieMarkForm


@login_required(login_url='/login/')
def view_art_nomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	nomination = ArtNomination.objects.get(pk=pk)
	pictures_1 = Picture.objects.filter(nomination=nomination, author__profile__category='1')
	pictures_2 = Picture.objects.filter(nomination=nomination, author__profile__category='2')
	pictures_3 = Picture.objects.filter(nomination=nomination, author__profile__category='3')
	pictures_4 = Picture.objects.filter(nomination=nomination, author__profile__category='4')

	marks_1 = PictureMark.objects.filter(work__in = pictures_1)
	marks_2 = PictureMark.objects.filter(work__in = pictures_2)
	marks_3 = PictureMark.objects.filter(work__in = pictures_3)
	marks_4 = PictureMark.objects.filter(work__in = pictures_4)

	ratings_1 = {}
	ratings_2 = {}
	ratings_3 = {}
	ratings_4 = {}
	pictures_list_1 = {}
	pictures_list_2 = {}
	pictures_list_3 = {}
	pictures_list_4 = {}

	for picture in pictures_1:
		mrks = marks_1.filter(work=picture)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
				summa += mark.criterai_four
				summa += mark.criterai_five
			summa = summa / length
			ratings_1[picture.id] = summa
		else:
			ratings_1[picture.id] = 0
		pictures_list_1[picture.id]=picture

	for picture in pictures_2:
		mrks = marks_2.filter(work=picture)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
				summa += mark.criterai_four
				summa += mark.criterai_five
			summa = summa / length
			ratings_2[picture.id] = summa;
		else:
			ratings_2[picture.id] = 0
		pictures_list_2[picture.id]=picture

	for picture in pictures_3:
		mrks = marks_3.filter(work=picture)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
				summa += mark.criterai_four
				summa += mark.criterai_five
			summa = summa / length
			ratings_3[picture.id] = summa;
		else:
			ratings_3[picture.id] = 0
		pictures_list_3[picture.id]=picture

	for picture in pictures_4:
		mrks = marks_4.filter(work=picture)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
				summa += mark.criterai_four
				summa += mark.criterai_five
			summa = summa / length
			ratings_4[picture.id] = summa;
		else:
			ratings_4[picture.id] = 0
		pictures_list_4[picture.id]=picture[picture.id]=picture


	sorting_1 = sorted(ratings_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2 = sorted(ratings_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3 = sorted(ratings_3.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4 = sorted(ratings_4.items(), key=operator.itemgetter(1), reverse=True)

	if request.POST:
		filename = translit.slugify(str(nomination)) + ' ('
		if 'type_1' in request.POST:
			pictures_list = pictures_list_1
			sorting = sorting_1
			name = 'Студенты учреждений среднего профессионального образовани'
			filename += 'students_spo (DPI)'
		elif  'type_2' in request.POST:
			pictures_list = pictures_list_2
			sorting = sorting_2
			name = 'Студенты высших учебных заведений'
			filename += 'students_spo (DPI)'
		elif  'type_3' in request.POST:
			pictures_list = pictures_list_3
			sorting = sorting_3
			name = 'Преподаватели, руководители коллективов'
			filename += 'teachers (DPI)'
		else:
			pictures_list = pictures_list_4
			sorting = sorting_4
			name = 'Любительские коллективы'
			filename += 'groups (DPI)'
		filename += ')'


		dte = date.today()
		document = Document()
		section = document.sections[-1]
		new_width, new_height = section.page_height, section.page_width
		section.orientation = WD_ORIENT.PORTRAIT
		section.page_width = Mm(297)
		section.page_height = Mm(210)
		section.left_margin = Mm(30)
		section.right_margin = Mm(10)
		section.top_margin = Mm(10)
		section.bottom_margin = Mm(10)
		section.header_distance = Mm(10)
		section.footer_distance = Mm(10)

		style = document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(12)


		document.add_paragraph(str(nomination) + ' (' + name + ')').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		table = document.add_table(rows=1, cols=7)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(20)
		table.columns[2].width = Mm(50)
		table.columns[3].width = Mm(50)
		table.columns[4].width = Mm(50)
		table.columns[5].width = Mm(50)
		table.columns[6].width = Mm(17)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Рег.номер'
		hdr_cells[1].width = Mm(20)
		hdr_cells[2].text = 'Название работы'
		hdr_cells[2].width = Mm(50)
		hdr_cells[3].text = 'Конкурсант'
		hdr_cells[3].width = Mm(50)
		hdr_cells[4].text = 'Преподаватель'
		hdr_cells[4].width = Mm(50)
		hdr_cells[5].text = 'Учреждение'
		hdr_cells[5].width = Mm(50)
		hdr_cells[6].text = 'Оценка'
		hdr_cells[6].width = Mm(17)


		cnt = 1
		for key, val in sorting:
			picture = pictures_list[key]

			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].width = Mm(10)
			row_cells[1].text = str(picture.author.id)
			row_cells[1].width = Mm(20)
			row_cells[2].text = picture.name
			row_cells[2].width = Mm(50)
			row_cells[3].text = picture.author.profile.get_full_name()
			row_cells[3].width = Mm(50)
			row_cells[4].text = picture.author.profile.get_teacher_full_name()
			row_cells[4].width = Mm(50)
			row_cells[5].text = picture.author.profile.institution
			row_cells[5].width = Mm(50)
			row_cells[6].text = str(val)
			row_cells[6].width = Mm(17)

			cnt += 1

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'nomination': nomination, 
		'pictures_list_1': pictures_list_1,
		'pictures_list_2': pictures_list_2,
		'pictures_list_3': pictures_list_3,
		'pictures_list_4': pictures_list_4,
		'sorting_1': sorting_1,
		'sorting_2': sorting_2,
		'sorting_3': sorting_3,
		'sorting_4': sorting_4,
	}
	return render(request, 'ratings/view_art_nominations.html', args)


@login_required(login_url='/login/')
def view_mov_nomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')


	nomination = VocalNomination.objects.get(pk=pk)
	movies_1 = Movie.objects.filter(nomination=nomination, author__profile__category='1')
	movies_2 = Movie.objects.filter(nomination=nomination, author__profile__category='2')
	movies_3 = Movie.objects.filter(nomination=nomination, author__profile__category='3')
	movies_4 = Movie.objects.filter(nomination=nomination, author__profile__category='4')

	marks_1 = MovieMark.objects.filter(work__in = movies_1)
	marks_2 = MovieMark.objects.filter(work__in = movies_2)
	marks_3 = MovieMark.objects.filter(work__in = movies_3)
	marks_4 = MovieMark.objects.filter(work__in = movies_4)

	ratings_1 = {}
	ratings_2 = {}
	ratings_3 = {}
	ratings_4 = {}
	movies_list_1 = {}
	movies_list_2 = {}
	movies_list_3 = {}
	movies_list_4 = {}

	for movie in movies_1:
		mrks = marks_1.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_1[movie.id] = summa
		else:
			ratings_1[movie.id] = 0
		movies_list_1[movie.id]=movie

	for movie in movies_2:
		mrks = marks_2.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_2[movie.id] = summa;
		else:
			ratings_2[movie.id] = 0
		movies_list_2[movie.id]=movie

	for movie in movies_3:
		mrks = marks_3.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_3[movie.id] = summa;
		else:
			ratings_3[movie.id] = 0
		movies_list_3[movie.id]=movie

	for movie in movies_4:
		mrks = marks_4.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_4[movie.id] = summa;
		else:
			ratings_4[movie.id] = 0
		movies_list_4[movie.id]=movie


	sorting_1 = sorted(ratings_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2 = sorted(ratings_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3 = sorted(ratings_3.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4 = sorted(ratings_4.items(), key=operator.itemgetter(1), reverse=True)

	if request.POST:
		filename = translit.slugify(str(nomination)) + ' ('
		if 'type_1' in request.POST:
			movies_list = movies_list_1
			sorting = sorting_1
			name = 'Студенты учреждений среднего профессионального образовани'
			filename += 'students_spo (vocal)'
		elif  'type_2' in request.POST:
			movies_list = movies_list_2
			sorting = sorting_2
			name = 'Студенты высших учебных заведений'
			filename += 'students_spo (vocal)'
		elif  'type_3' in request.POST:
			movies_list = movies_list_3
			sorting = sorting_3
			name = 'Преподаватели, руководители коллективов'
			filename += 'teachers (vocal)'
		else:
			movies_list = movies_list_4
			sorting = sorting_4
			name = 'Любительские коллективы'
			filename += 'groups (vocal)'
		filename += ')'


		dte = date.today()
		document = Document()
		section = document.sections[-1]
		new_width, new_height = section.page_height, section.page_width
		section.orientation = WD_ORIENT.PORTRAIT
		section.page_width = Mm(297)
		section.page_height = Mm(210)
		section.left_margin = Mm(30)
		section.right_margin = Mm(10)
		section.top_margin = Mm(10)
		section.bottom_margin = Mm(10)
		section.header_distance = Mm(10)
		section.footer_distance = Mm(10)

		style = document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(12)


		document.add_paragraph(str(nomination) + ' (' + name + ')').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		table = document.add_table(rows=1, cols=7)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(20)
		table.columns[2].width = Mm(50)
		table.columns[3].width = Mm(50)
		table.columns[4].width = Mm(50)
		table.columns[5].width = Mm(50)
		table.columns[6].width = Mm(17)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Рег.номер'
		hdr_cells[1].width = Mm(20)
		hdr_cells[2].text = 'Название работы'
		hdr_cells[2].width = Mm(50)
		hdr_cells[3].text = 'Конкурсант(Коллектив)'
		hdr_cells[3].width = Mm(50)
		hdr_cells[4].text = 'Преподаватель/Концертмейстер'
		hdr_cells[4].width = Mm(50)
		hdr_cells[5].text = 'Учреждение'
		hdr_cells[5].width = Mm(50)
		hdr_cells[6].text = 'Оценка'
		hdr_cells[6].width = Mm(17)


		cnt = 1
		for key, val in sorting:
			movie = movies_list[key]

			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].width = Mm(10)
			row_cells[1].text = str(movie.author.id)
			row_cells[1].width = Mm(20)
			row_cells[2].text = movie.name
			row_cells[2].width = Mm(50)
			row_cells[3].text = movie.author.profile.get_full_name()
			if movie.author.profile.group:
				row_cells[3].text += ' (' + movie.author.profile.group + ')'
			row_cells[3].width = Mm(50)
			row_cells[4].text = ''
			if movie.author.profile.surname_teacher:
				row_cells[4].text += 'Преп.: ' + movie.author.profile.get_teacher_full_name()
			if movie.author.profile.surname_musician:
				row_cells[4].text += ' Конц.: ' + movie.author.profile.get_musician_full_name()
			row_cells[4].width = Mm(50)
			row_cells[5].text = movie.author.profile.institution
			row_cells[5].width = Mm(50)
			row_cells[6].text = str(val)
			row_cells[6].width = Mm(17)

			cnt += 1

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'nomination': nomination, 
		'movies_list_1': movies_list_1,
		'movies_list_2': movies_list_2,
		'movies_list_3': movies_list_3,
		'movies_list_4': movies_list_4,
		'sorting_1': sorting_1,
		'sorting_2': sorting_2,
		'sorting_3': sorting_3,
		'sorting_4': sorting_4,
	}
	return render(request, 'ratings/view_mov_nominations.html', args)