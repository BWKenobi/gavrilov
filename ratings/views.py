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

from pictures.models import Picture, CoPicturee
from movies.models import Movie, CoMovie
from nominations.models import ArtNomination, VocalNomination
from marks.models import PictureMark, MovieMark

from marks.forms import PictureMarkForm, MovieMarkForm


@login_required(login_url='/login/')
def view_art_nomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	nomination = ArtNomination.objects.get(pk=pk)

	pictures_all = Picture.objects.filter(nomination=nomination)
	copictures = {}
	for picture_all in pictures_all:
		copictures[picture_all.pk] = CoPicturee.objects.filter(picture=picture_all)

	pictures_1_1 = Picture.objects.filter(nomination=nomination, author__profile__category='1', author__profile__participation='1')
	pictures_2_1 = Picture.objects.filter(nomination=nomination, author__profile__category='2', author__profile__participation='1')
	pictures_3_1 = Picture.objects.filter(nomination=nomination, author__profile__category='3', author__profile__participation='1')
	pictures_4_1 = Picture.objects.filter(nomination=nomination, author__profile__category='4', author__profile__participation='1')
	pictures_1_2 = Picture.objects.filter(nomination=nomination, author__profile__category='1', author__profile__participation='2')
	pictures_2_2 = Picture.objects.filter(nomination=nomination, author__profile__category='2', author__profile__participation='2')
	pictures_3_2 = Picture.objects.filter(nomination=nomination, author__profile__category='3', author__profile__participation='2')
	pictures_4_2 = Picture.objects.filter(nomination=nomination, author__profile__category='4', author__profile__participation='2')

	marks_1_1 = PictureMark.objects.filter(work__in = pictures_1_1)
	marks_2_1 = PictureMark.objects.filter(work__in = pictures_2_1)
	marks_3_1 = PictureMark.objects.filter(work__in = pictures_3_1)
	marks_4_1 = PictureMark.objects.filter(work__in = pictures_4_1)
	marks_1_2 = PictureMark.objects.filter(work__in = pictures_1_2)
	marks_2_2 = PictureMark.objects.filter(work__in = pictures_2_2)
	marks_3_2 = PictureMark.objects.filter(work__in = pictures_3_2)
	marks_4_2 = PictureMark.objects.filter(work__in = pictures_4_2)

	ratings_1_1 = {}
	ratings_2_1 = {}
	ratings_3_1 = {}
	ratings_4_1 = {}
	ratings_1_2 = {}
	ratings_2_2 = {}
	ratings_3_2 = {}
	ratings_4_2 = {}
	pictures_list_1_1 = {}
	pictures_list_2_1 = {}
	pictures_list_3_1 = {}
	pictures_list_4_1 = {}
	pictures_list_1_2 = {}
	pictures_list_2_2 = {}
	pictures_list_3_2 = {}
	pictures_list_4_2 = {}

	for picture in pictures_1_1:
		mrks = marks_1_1.filter(work=picture)
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
			ratings_1_1[picture.id] = round(summa, 1)
		else:
			ratings_1_1[picture.id] = 0
		pictures_list_1_1[picture.id]=picture

	for picture in pictures_2_1:
		mrks = marks_2_1.filter(work=picture)
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
			ratings_2_1[picture.id] = round(summa, 1)
		else:
			ratings_2_1[picture.id] = 0
		pictures_list_2_1[picture.id]=picture

	for picture in pictures_3_1:
		mrks = marks_3_1.filter(work=picture)
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
			ratings_3_1[picture.id] = round(summa, 1)
		else:
			ratings_3_1[picture.id] = 0
		pictures_list_3_1[picture.id]=picture

	for picture in pictures_4_1:
		mrks = marks_4_1.filter(work=picture)
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
			ratings_4_1[picture.id] = round(summa, 1)
		else:
			ratings_4_1[picture.id] = 0
		pictures_list_4_1[picture.id]=picture


########################################################
	for picture in pictures_1_2:
		mrks = marks_1_2.filter(work=picture)
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
			ratings_1_2[picture.id] = round(summa, 1)
		else:
			ratings_1_2[picture.id] = 0
		pictures_list_1_2[picture.id]=picture

	for picture in pictures_2_2:
		mrks = marks_2_2.filter(work=picture)
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
			ratings_2_2[picture.id] = round(summa, 1)
		else:
			ratings_2_2[picture.id] = 0
		pictures_list_2_2[picture.id]=picture

	for picture in pictures_3_2:
		mrks = marks_3_2.filter(work=picture)
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
			ratings_3_2[picture.id] = round(summa, 1)
		else:
			ratings_3_2[picture.id] = 0
		pictures_list_3_2[picture.id]=picture

	for picture in pictures_4_2:
		mrks = marks_4_2.filter(work=picture)
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
			ratings_4_2[picture.id] = round(summa, 1)
		else:
			ratings_4_2[picture.id] = 0
		pictures_list_4_2[picture.id]=picture

	sorting_1_1 = sorted(ratings_1_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2_1 = sorted(ratings_2_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3_1 = sorted(ratings_3_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4_1 = sorted(ratings_4_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_1_2 = sorted(ratings_1_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2_2 = sorted(ratings_2_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3_2 = sorted(ratings_3_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4_2 = sorted(ratings_4_2.items(), key=operator.itemgetter(1), reverse=True)

	if request.POST:
		filename = translit.slugify(str(nomination)) + ' ('
		if 'type_1_1' in request.POST:
			pictures_list = pictures_list_1_1
			sorting = sorting_1_1
			name = 'Студенты учреждений среднего профессионального образовани (очное участие)'
			filename += 'students_spo_ochno (DPI)'
		elif 'type_1_2' in request.POST:
			pictures_list = pictures_list_1_2
			sorting = sorting_1_2
			name = 'Студенты учреждений среднего профессионального образовани (заочное участие)'
			filename += 'students_spo_zaochno (DPI)'
		elif  'type_2_1' in request.POST:
			pictures_list = pictures_list_2_1
			sorting = sorting_2_1
			name = 'Студенты высших учебных заведений (очное участие)'
			filename += 'students_vpo_ochno (DPI)'
		elif  'type_2_2' in request.POST:
			pictures_list = pictures_list_2_2
			sorting = sorting_2_2
			name = 'Студенты высших учебных заведений (заочное участие)'
			filename += 'students_vpo_zaochno (DPI)'
		elif  'type_3_1' in request.POST:
			pictures_list = pictures_list_3_1
			sorting = sorting_3_1
			name = 'Преподаватели, руководители коллективов (очное участие)'
			filename += 'teachers_ochno (DPI)'
		elif  'type_3_2' in request.POST:
			pictures_list = pictures_list_3_2
			sorting = sorting_3_2
			name = 'Преподаватели, руководители коллективов (заочное участие)'
			filename += 'teachers_zaochno (DPI)'
		elif  'type_4_1' in request.POST:
			pictures_list = pictures_list_4_1
			sorting = sorting_4_1
			name = 'Любительские коллективы (очное участие)'
			filename += 'groups_ochno (DPI)'
		else:
			pictures_list = pictures_list_4_2
			sorting = sorting_4_2
			name = 'Любительские коллективы (заочное участие)'
			filename += 'groups_zaochno (DPI)'
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

		table = document.add_table(rows=1, cols=6)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(60)
		table.columns[2].width = Mm(60)
		table.columns[3].width = Mm(50)
		table.columns[4].width = Mm(50)
		table.columns[5].width = Mm(17)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Название работы'
		hdr_cells[1].width = Mm(60)
		hdr_cells[2].text = 'Конкурсант'
		hdr_cells[2].width = Mm(60)
		hdr_cells[3].text = 'Преподаватель'
		hdr_cells[3].width = Mm(50)
		hdr_cells[4].text = 'Учреждение'
		hdr_cells[4].width = Mm(50)
		hdr_cells[5].text = 'Оценка'
		hdr_cells[5].width = Mm(17)


		cnt = 1
		for key, val in sorting:
			picture = pictures_list[key]

			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].width = Mm(10)
			row_cells[1].text = picture.name
			row_cells[1].width = Mm(60)
			row_cells[2].text = picture.author.profile.get_full_name()
			row_cells[2].width = Mm(60)
			row_cells[3].text = ''
			for copicture in copictures[key]:
				row_cells[3].text += copicture.coauthor.get_file_name() + '(' + copicture.coauthor.get_profile_type_display() + ')'
			row_cells[3].width = Mm(50)
			row_cells[4].text = picture.author.profile.institution
			row_cells[4].width = Mm(50)
			row_cells[5].text = str(val)
			row_cells[5].width = Mm(17)

			cnt += 1

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'nomination': nomination, 
		'pictures_list_1_1': pictures_list_1_1,
		'pictures_list_2_1': pictures_list_2_1,
		'pictures_list_3_1': pictures_list_3_1,
		'pictures_list_4_1': pictures_list_4_1,
		'pictures_list_1_2': pictures_list_1_2,
		'pictures_list_2_2': pictures_list_2_2,
		'pictures_list_3_2': pictures_list_3_2,
		'pictures_list_4_2': pictures_list_4_2,
		'sorting_1_1': sorting_1_1,
		'sorting_2_1': sorting_2_1,
		'sorting_3_1': sorting_3_1,
		'sorting_4_1': sorting_4_1,
		'sorting_1_2': sorting_1_2,
		'sorting_2_2': sorting_2_2,
		'sorting_3_2': sorting_3_2,
		'sorting_4_2': sorting_4_2,
		'copictures': copictures
	}
	return render(request, 'ratings/view_art_nominations.html', args)


@login_required(login_url='/login/')
def view_mov_nomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')


	nomination = VocalNomination.objects.get(pk=pk)

	movies_all = Movie.objects.filter(nomination=nomination)
	comovies = {}
	for move_all in movies_all:
		comovies[move_all.pk] = CoMovie.objects.filter(movie=move_all)


	movies_1_1 = Movie.objects.filter(nomination=nomination, author__profile__category='1', author__profile__participation='1')
	movies_2_1 = Movie.objects.filter(nomination=nomination, author__profile__category='2', author__profile__participation='1')
	movies_3_1 = Movie.objects.filter(nomination=nomination, author__profile__category='3', author__profile__participation='1')
	movies_4_1 = Movie.objects.filter(nomination=nomination, author__profile__category='4', author__profile__participation='1')
	movies_1_2 = Movie.objects.filter(nomination=nomination, author__profile__category='1', author__profile__participation='2')
	movies_2_2 = Movie.objects.filter(nomination=nomination, author__profile__category='2', author__profile__participation='2')
	movies_3_2 = Movie.objects.filter(nomination=nomination, author__profile__category='3', author__profile__participation='2')
	movies_4_2 = Movie.objects.filter(nomination=nomination, author__profile__category='4', author__profile__participation='2')

	marks_1_1 = MovieMark.objects.filter(work__in = movies_1_1)
	marks_2_1 = MovieMark.objects.filter(work__in = movies_2_1)
	marks_3_1 = MovieMark.objects.filter(work__in = movies_3_1)
	marks_4_1 = MovieMark.objects.filter(work__in = movies_4_1)
	marks_1_2 = MovieMark.objects.filter(work__in = movies_1_2)
	marks_2_2 = MovieMark.objects.filter(work__in = movies_2_2)
	marks_3_2 = MovieMark.objects.filter(work__in = movies_3_2)
	marks_4_2 = MovieMark.objects.filter(work__in = movies_4_2)

	ratings_1_1 = {}
	ratings_2_1 = {}
	ratings_3_1 = {}
	ratings_4_1 = {}
	ratings_1_2 = {}
	ratings_2_2 = {}
	ratings_3_2 = {}
	ratings_4_2 = {}
	movies_list_1_1 = {}
	movies_list_2_1 = {}
	movies_list_3_1 = {}
	movies_list_4_1 = {}
	movies_list_1_2 = {}
	movies_list_2_2 = {}
	movies_list_3_2 = {}
	movies_list_4_2 = {}

	for movie in movies_1_1:
		mrks = marks_1_1.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_1_1[movie.id] = round(summa, 1)
		else:
			ratings_1_1[movie.id] = 0
		movies_list_1_1[movie.id]=movie

	for movie in movies_2_1:
		mrks = marks_2_1.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_2_1[movie.id] = round(summa, 1)
		else:
			ratings_2_1[movie.id] = 0
		movies_list_2_1[movie.id]=movie

	for movie in movies_3_1:
		mrks = marks_3_1.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_3_1[movie.id] = round(summa, 1)
		else:
			ratings_3_1[movie.id] = 0
		movies_list_3_1[movie.id]=movie

	for movie in movies_4_1:
		mrks = marks_4_1.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_4_1[movie.id] = round(summa, 1)
		else:
			ratings_4_1[movie.id] = 0
		movies_list_4_1[movie.id]=movie

########################################################
	for movie in movies_1_2:
		mrks = marks_1_2.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_1_2[movie.id] = round(summa, 1)
		else:
			ratings_1_2[movie.id] = 0
		movies_list_1_2[movie.id]=movie

	for movie in movies_2_2:
		mrks = marks_2_2.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_2_2[movie.id] = round(summa, 1)
		else:
			ratings_2_2[movie.id] = 0
		movies_list_2_2[movie.id]=movie

	for movie in movies_3_2:
		mrks = marks_3_2.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_3_2[movie.id] = round(summa, 1)
		else:
			ratings_3_2[movie.id] = 0
		movies_list_3_2[movie.id]=movie

	for movie in movies_4_2:
		mrks = marks_4_2.filter(work=movie)
		if mrks:
			length = len(mrks)
			summa = 0;
			for mark in mrks:
				summa += mark.criterai_one
				summa += mark.criterai_two
				summa += mark.criterai_three
			summa = summa / length
			ratings_4_2[movie.id] = round(summa, 1)
		else:
			ratings_4_2[movie.id] = 0
		movies_list_4_2[movie.id]=movie


	sorting_1_1 = sorted(ratings_1_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2_1 = sorted(ratings_2_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3_1 = sorted(ratings_3_1.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4_1 = sorted(ratings_4_1.items(), key=operator.itemgetter(1), reverse=True)

	sorting_1_2 = sorted(ratings_1_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_2_2 = sorted(ratings_2_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_3_2 = sorted(ratings_3_2.items(), key=operator.itemgetter(1), reverse=True)
	sorting_4_2 = sorted(ratings_4_2.items(), key=operator.itemgetter(1), reverse=True)

	if request.POST:
		filename = translit.slugify(str(nomination)) + ' ('
		if 'type_1_1' in request.POST:
			movies_list = movies_list_1_1
			sorting = sorting_1_1
			name = 'Студенты учреждений среднего профессионального образовани (очное участие)'
			filename += 'students_spo_ochno (vocal)'
		elif 'type_1_2' in request.POST:
			movies_list = movies_list_1_2
			sorting = sorting_1_2
			name = 'Студенты учреждений среднего профессионального образовани (заочное участие)'
			filename += 'students_spo_zaochno (vocal)'
		elif  'type_2_1' in request.POST:
			movies_list = movies_list_2_1
			sorting = sorting_2_1
			name = 'Студенты высших учебных заведений (очное участие)'
			filename += 'students_vpo_ochno (vocal)'
		elif  'type_2_2' in request.POST:
			movies_list = movies_list_2_2
			sorting = sorting_2_2
			name = 'Студенты высших учебных заведений (заочное участие)'
			filename += 'students_vpo_zaochno (vocal)'
		elif  'type_3_1' in request.POST:
			movies_list = movies_list_3_1
			sorting = sorting_3_1
			name = 'Преподаватели, руководители коллективов (очное участие)'
			filename += 'teachers_ochno (vocal)'
		elif  'type_3_2' in request.POST:
			movies_list = movies_list_3_2
			sorting = sorting_3_2
			name = 'Преподаватели, руководители коллективов (заочное участие)'
			filename += 'teachers_zaochno (vocal)'
		elif  'type_4_1' in request.POST:
			movies_list = movies_list_4_1
			sorting = sorting_4_1
			name = 'Любительские коллективы (очное участие)'
			filename += 'groups_ochno (vocal)'
		else:
			movies_list = movies_list_4_2
			sorting = sorting_4_2
			name = 'Любительские коллективы (заочное участие)'
			filename += 'groups_zaochno (vocal)'
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

		table = document.add_table(rows=1, cols=6)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(60)
		table.columns[2].width = Mm(60)
		table.columns[3].width = Mm(50)
		table.columns[4].width = Mm(50)
		table.columns[5].width = Mm(17)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Название работы'
		hdr_cells[1].width = Mm(60)
		hdr_cells[2].text = 'Конкурсант(Коллектив)'
		hdr_cells[2].width = Mm(60)
		hdr_cells[3].text = 'Преподаватель/Концертмейстер'
		hdr_cells[3].width = Mm(50)
		hdr_cells[4].text = 'Учреждение'
		hdr_cells[4].width = Mm(50)
		hdr_cells[5].text = 'Оценка'
		hdr_cells[5].width = Mm(17)


		cnt = 1
		for key, val in sorting:
			movie = movies_list[key]

			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].width = Mm(10)
			row_cells[1].text = movie.name
			row_cells[1].width = Mm(60)
			row_cells[2].text = movie.author.profile.get_full_name()
			if movie.author.profile.group:
				row_cells[2].text += ' (' + movie.author.profile.group + ')'
			row_cells[2].width = Mm(60)
			row_cells[3].text = ''
			for comove in comovies[key]:
				row_cells[3].text += comove.coauthor.get_file_name() + '(' + comove.coauthor.get_profile_type_display() + ')'
			row_cells[3].width = Mm(50)
			row_cells[4].text = movie.author.profile.institution
			row_cells[4].width = Mm(50)
			row_cells[5].text = str(val)
			row_cells[5].width = Mm(17)

			cnt += 1

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'nomination': nomination, 
		'movies_list_1_1': movies_list_1_1,
		'movies_list_2_1': movies_list_2_1,
		'movies_list_3_1': movies_list_3_1,
		'movies_list_4_1': movies_list_4_1,
		'movies_list_1_2': movies_list_1_2,
		'movies_list_2_2': movies_list_2_2,
		'movies_list_3_2': movies_list_3_2,
		'movies_list_4_2': movies_list_4_2,
		'sorting_1_1': sorting_1_1,
		'sorting_2_1': sorting_2_1,
		'sorting_3_1': sorting_3_1,
		'sorting_4_1': sorting_4_1,
		'sorting_1_2': sorting_1_2,
		'sorting_2_2': sorting_2_2,
		'sorting_3_2': sorting_3_2,
		'sorting_4_2': sorting_4_2,
		'comovies': comovies
	}
	return render(request, 'ratings/view_mov_nominations.html', args)