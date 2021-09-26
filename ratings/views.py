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
from nominations.models import ArtNomination, VocalNomination
from marks.models import PictureMark, MasterMark

from marks.forms import PictureMarkForm, MasterMarkForm


@login_required(login_url='/login/')
def view_nomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	# nomination = Nomination.objects.get(pk=pk)
	# pictures_1 = Picture.objects.filter(nomination=nomination, author__group='3')
	# pictures_2 = Picture.objects.filter(nomination=nomination, author__group='4')
	# pictures_3 = Picture.objects.filter(nomination=nomination, author__group='1')
	# pictures_4 = Picture.objects.filter(nomination=nomination, author__group='2')

	# marks_1 = PictureMark.objects.filter(work__in = pictures_1)
	# marks_2 = PictureMark.objects.filter(work__in = pictures_2)
	# marks_3 = PictureMark.objects.filter(work__in = pictures_3)
	# marks_4 = PictureMark.objects.filter(work__in = pictures_4)

	# ratings_1 = {}
	# ratings_2 = {}
	# ratings_3 = {}
	# ratings_4 = {}
	# pictures_list_1 = {}
	# pictures_list_2 = {}
	# pictures_list_3 = {}
	# pictures_list_4 = {}

	# for picture in pictures_1:
	# 	mrks = marks_1.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_1[picture.id] = summa
	# 	else:
	# 		ratings_1[picture.id] = 0
	# 	pictures_list_1[picture.id]=picture

	# for picture in pictures_2:
	# 	mrks = marks_2.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_2[picture.id] = summa;
	# 	else:
	# 		ratings_2[picture.id] = 0
	# 	pictures_list_2[picture.id]=picture

	# for picture in pictures_3:
	# 	mrks = marks_3.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_3[picture.id] = summa;
	# 	else:
	# 		ratings_3[picture.id] = 0
	# 	pictures_list_3[picture.id]=picture

	# for picture in pictures_4:
	# 	mrks = marks_4.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_4[picture.id] = summa;
	# 	else:
	# 		ratings_4[picture.id] = 0
	# 	pictures_list_4[picture.id]=picture[picture.id]=picture


	# sorting_1 = sorted(ratings_1.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_2 = sorted(ratings_2.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_3 = sorted(ratings_3.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_4 = sorted(ratings_4.items(), key=operator.itemgetter(1), reverse=True)

	# if request.POST:
	# 	filename = translit.slugify(str(nomination)) + ' ('
	# 	if 'type_1' in request.POST:
	# 		pictures_list = pictures_list_1
	# 		sorting = sorting_1
	# 		name = 'ДШИ, ДХШ (13-14 лет)'
	# 		filename += 'dshi-13-14'
	# 	elif  'type_2' in request.POST:
	# 		pictures_list = pictures_list_2
	# 		sorting = sorting_2
	# 		name = 'ДШИ, ДХШ (от 15 лет)'
	# 		filename += 'dshi-15'
	# 	elif  'type_3' in request.POST:
	# 		pictures_list = pictures_list_3
	# 		sorting = sorting_3
	# 		name = 'Студенты СПО'
	# 		filename += 'spo'
	# 	else:
	# 		pictures_list = pictures_list_4
	# 		sorting = sorting_4
	# 		name = 'Студенты ВПО'
	# 		filename += 'vpo'
	# 	filename += ')'


	# 	dte = date.today()
	# 	document = Document()
	# 	section = document.sections[-1]
	# 	new_width, new_height = section.page_height, section.page_width
	# 	section.orientation = WD_ORIENT.PORTRAIT
	# 	section.page_width = Mm(297)
	# 	section.page_height = Mm(210)
	# 	section.left_margin = Mm(30)
	# 	section.right_margin = Mm(10)
	# 	section.top_margin = Mm(10)
	# 	section.bottom_margin = Mm(10)
	# 	section.header_distance = Mm(10)
	# 	section.footer_distance = Mm(10)

	# 	style = document.styles['Normal']
	# 	font = style.font
	# 	font.name = 'Times New Roman'
	# 	font.size = Pt(12)


	# 	document.add_paragraph(str(nomination) + ' (' + name + ')').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
	# 	p = document.add_paragraph()
	# 	p.add_run(dte.strftime('%d.%b.%Y')).italic = True
	# 	p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

	# 	table = document.add_table(rows=1, cols=7)
	# 	table.allow_autifit = False
	# 	table.style = 'TableGrid'
	# 	table.columns[0].width = Mm(10)
	# 	table.columns[1].width = Mm(20)
	# 	table.columns[2].width = Mm(50)
	# 	table.columns[3].width = Mm(50)
	# 	table.columns[4].width = Mm(50)
	# 	table.columns[5].width = Mm(50)
	# 	table.columns[6].width = Mm(17)

	# 	hdr_cells = table.rows[0].cells
	# 	hdr_cells[0].text = '№'
	# 	hdr_cells[0].width = Mm(10)
	# 	hdr_cells[1].text = 'Рег.номер'
	# 	hdr_cells[1].width = Mm(20)
	# 	hdr_cells[2].text = 'Название работы'
	# 	hdr_cells[2].width = Mm(50)
	# 	hdr_cells[3].text = 'Конкурсант'
	# 	hdr_cells[3].width = Mm(50)
	# 	hdr_cells[4].text = 'Преподаватель'
	# 	hdr_cells[4].width = Mm(50)
	# 	hdr_cells[5].text = 'Учреждение'
	# 	hdr_cells[5].width = Mm(50)
	# 	hdr_cells[6].text = 'Оценка'
	# 	hdr_cells[6].width = Mm(17)


	# 	cnt = 1
	# 	for key, val in sorting:
	# 		picture = pictures_list[key]

	# 		row_cells = table.add_row().cells
	# 		row_cells[0].text = str(cnt)
	# 		row_cells[0].width = Mm(10)
	# 		row_cells[1].text = str(picture.author.id)
	# 		row_cells[1].width = Mm(20)
	# 		row_cells[2].text = picture.name
	# 		row_cells[2].width = Mm(50)
	# 		row_cells[3].text = picture.author.get_full_name()
	# 		row_cells[3].width = Mm(50)
	# 		if picture.author.teacher_plus_flag:
	# 			row_cells[4].text = picture.author.teacher_plus.get_full_name()
	# 		else:
	# 			row_cells[4].text = picture.author.teacher.profile.get_full_name()
	# 		row_cells[4].width = Mm(50)
	# 		row_cells[5].text = picture.author.teacher.profile.institution
	# 		row_cells[5].width = Mm(50)
	# 		row_cells[6].text = str(val)
	# 		row_cells[6].width = Mm(17)

	# 		cnt += 1

	# 	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
	# 	response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
	# 	document.save(response)

	# 	return response

	# args = {
	# 	'nomination': nomination, 
	# 	'pictures_list_1': pictures_list_1,
	# 	'pictures_list_2': pictures_list_2,
	# 	'pictures_list_3': pictures_list_3,
	# 	'pictures_list_4': pictures_list_4,
	# 	'sorting_1': sorting_1,
	# 	'sorting_2': sorting_2,
	# 	'sorting_3': sorting_3,
	# 	'sorting_4': sorting_4,
	# }
	# return render(request, 'ratings/view_nominations.html', args)


@login_required(login_url='/login/')
def view_subnomination(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	# subnomination = SubNomination.objects.get(pk=pk)
	# nomination = subnomination.nomination

	# pictures_1 = Picture.objects.filter(subnomination=subnomination, author__group='3')
	# pictures_2 = Picture.objects.filter(subnomination=subnomination, author__group='4')
	# pictures_3 = Picture.objects.filter(subnomination=subnomination, author__group='1')
	# pictures_4 = Picture.objects.filter(subnomination=subnomination, author__group='2')

	# marks_1 = PictureMark.objects.filter(work__in = pictures_1)
	# marks_2 = PictureMark.objects.filter(work__in = pictures_2)
	# marks_3 = PictureMark.objects.filter(work__in = pictures_3)
	# marks_4 = PictureMark.objects.filter(work__in = pictures_4)

	# ratings_1 = {}
	# ratings_2 = {}
	# ratings_3 = {}
	# ratings_4 = {}
	# pictures_list_1 = {}
	# pictures_list_2 = {}
	# pictures_list_3 = {}
	# pictures_list_4 = {}

	# for picture in pictures_1:
	# 	mrks = marks_1.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_1[picture.id] = summa
	# 	else:
	# 		ratings_1[picture.id] = 0
	# 	pictures_list_1[picture.id]=picture

	# for picture in pictures_2:
	# 	mrks = marks_2.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_2[picture.id] = summa;
	# 	else:
	# 		ratings_2[picture.id] = 0
	# 	pictures_list_2[picture.id]=picture

	# for picture in pictures_3:
	# 	mrks = marks_3.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_3[picture.id] = summa;
	# 	else:
	# 		ratings_3[picture.id] = 0
	# 	pictures_list_3[picture.id]=picture

	# for picture in pictures_4:
	# 	mrks = marks_4.filter(work=picture)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_4[picture.id] = summa;
	# 	else:
	# 		ratings_4[picture.id] = 0
	# 	pictures_list_4[picture.id]=picture[picture.id]=picture


	# sorting_1 = sorted(ratings_1.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_2 = sorted(ratings_2.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_3 = sorted(ratings_3.items(), key=operator.itemgetter(1), reverse=True)
	# sorting_4 = sorted(ratings_4.items(), key=operator.itemgetter(1), reverse=True)

	# if request.POST:
	# 	filename = translit.slugify(str(nomination)) + '-' + translit.slugify(str(subnomination)) + ' ('
	# 	if 'type_1' in request.POST:
	# 		pictures_list = pictures_list_1
	# 		sorting = sorting_1
	# 		name = 'ДШИ, ДХШ (13-14 лет)'
	# 		filename += 'dshi-13-14'
	# 	elif  'type_2' in request.POST:
	# 		pictures_list = pictures_list_2
	# 		sorting = sorting_2
	# 		name = 'ДШИ, ДХШ (от 15 лет)'
	# 		filename += 'dshi-15'
	# 	elif  'type_3' in request.POST:
	# 		pictures_list = pictures_list_3
	# 		sorting = sorting_3
	# 		name = 'Студенты СПО'
	# 		filename += 'spo'
	# 	else:
	# 		pictures_list = pictures_list_4
	# 		sorting = sorting_4
	# 		name = 'Студенты ВПО'
	# 		filename += 'vpo'
	# 	filename += ')'


	# 	dte = date.today()
	# 	document = Document()
	# 	section = document.sections[-1]
	# 	new_width, new_height = section.page_height, section.page_width
	# 	section.orientation = WD_ORIENT.PORTRAIT
	# 	section.page_width = Mm(297)
	# 	section.page_height = Mm(210)
	# 	section.left_margin = Mm(30)
	# 	section.right_margin = Mm(10)
	# 	section.top_margin = Mm(10)
	# 	section.bottom_margin = Mm(10)
	# 	section.header_distance = Mm(10)
	# 	section.footer_distance = Mm(10)

	# 	style = document.styles['Normal']
	# 	font = style.font
	# 	font.name = 'Times New Roman'
	# 	font.size = Pt(12)


	# 	document.add_paragraph(str(nomination) + '-' + str(subnomination) +' (' + name + ')').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
	# 	p = document.add_paragraph()
	# 	p.add_run(dte.strftime('%d.%b.%Y')).italic = True
	# 	p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

	# 	table = document.add_table(rows=1, cols=7)
	# 	table.allow_autifit = False
	# 	table.style = 'TableGrid'
	# 	table.columns[0].width = Mm(10)
	# 	table.columns[1].width = Mm(20)
	# 	table.columns[2].width = Mm(50)
	# 	table.columns[3].width = Mm(50)
	# 	table.columns[4].width = Mm(50)
	# 	table.columns[5].width = Mm(50)
	# 	table.columns[6].width = Mm(17)

	# 	hdr_cells = table.rows[0].cells
	# 	hdr_cells[0].text = '№'
	# 	hdr_cells[0].width = Mm(10)
	# 	hdr_cells[1].text = 'Рег.номер'
	# 	hdr_cells[1].width = Mm(20)
	# 	hdr_cells[2].text = 'Название работы'
	# 	hdr_cells[2].width = Mm(50)
	# 	hdr_cells[3].text = 'Конкурсант'
	# 	hdr_cells[3].width = Mm(50)
	# 	hdr_cells[4].text = 'Преподаватель'
	# 	hdr_cells[4].width = Mm(50)
	# 	hdr_cells[5].text = 'Учреждение'
	# 	hdr_cells[5].width = Mm(50)
	# 	hdr_cells[6].text = 'Оценка'
	# 	hdr_cells[6].width = Mm(17)


	# 	cnt = 1
	# 	for key, val in sorting:
	# 		picture = pictures_list[key]

	# 		row_cells = table.add_row().cells
	# 		row_cells[0].text = str(cnt)
	# 		row_cells[0].width = Mm(10)
	# 		row_cells[1].text = str(picture.author.id)
	# 		row_cells[1].width = Mm(20)
	# 		row_cells[2].text = picture.name
	# 		row_cells[2].width = Mm(50)
	# 		row_cells[3].text = picture.author.get_full_name()
	# 		row_cells[3].width = Mm(50)
	# 		if picture.author.teacher_plus_flag:
	# 			row_cells[4].text = picture.author.teacher_plus.get_full_name()
	# 		else:
	# 			row_cells[4].text = picture.author.teacher.profile.get_full_name()
	# 		row_cells[4].width = Mm(50)
	# 		row_cells[5].text = picture.author.teacher.profile.institution
	# 		row_cells[5].width = Mm(50)
	# 		row_cells[6].text = str(val)
	# 		row_cells[6].width = Mm(17)

	# 		cnt += 1

	# 	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
	# 	response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
	# 	document.save(response)

	# 	return response

	# args = {
	# 	'subnomination': subnomination, 
	# 	'pictures_list_1': pictures_list_1,
	# 	'pictures_list_2': pictures_list_2,
	# 	'pictures_list_3': pictures_list_3,
	# 	'pictures_list_4': pictures_list_4,
	# 	'sorting_1': sorting_1,
	# 	'sorting_2': sorting_2,
	# 	'sorting_3': sorting_3,
	# 	'sorting_4': sorting_4,
	# }
	# return render(request, 'ratings/view_subnominations.html', args)



@login_required(login_url='/login/')
def view_master(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	# children_1 = Child.objects.filter(master_flag=True, group='3')
	# children_2 = Child.objects.filter(master_flag=True, group='4')
	# children_3 = Child.objects.filter(master_flag=True, group='1')
	# children_4 = Child.objects.filter(master_flag=True, group='2')
	# marks = MasterMark.objects.all()

	# ratings_1 = {}
	# ratings_2 = {}
	# ratings_3 = {}
	# ratings_4 = {}
	# children_list_1 = {}
	# children_list_2 = {}
	# children_list_3 = {}
	# children_list_4 = {}

	# for child in children_1:
	# 	mrks = marks.filter(work=child)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_1[child.id] = summa
	# 	else:
	# 		ratings_1[child.id] = 0

	# 	children_list_1[child.id] = child
	
	# sorting_1 = sorted(ratings_1.items(), key=operator.itemgetter(1), reverse=True)



	# for child in children_2:
	# 	mrks = marks.filter(work=child)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_2[child.id] = summa
	# 	else:
	# 		ratings_2[child.id] = 0

	# 	children_list_2[child.id] = child
	
	# sorting_2 = sorted(ratings_2.items(), key=operator.itemgetter(1), reverse=True)



	# for child in children_3:
	# 	mrks = marks.filter(work=child)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_3[child.id] = summa
	# 	else:
	# 		ratings_3[child.id] = 0

	# 	children_list_3[child.id] = child
	
	# sorting_3 = sorted(ratings_3.items(), key=operator.itemgetter(1), reverse=True)



	# for child in children_4:
	# 	mrks = marks.filter(work=child)
	# 	if mrks:
	# 		length = len(mrks)
	# 		summa = 0;
	# 		for mark in mrks:
	# 			summa += mark.criterai_one
	# 			summa += mark.criterai_two
	# 			summa += mark.criterai_three
	# 			summa += mark.criterai_four
	# 			summa += mark.criterai_five
	# 		summa = summa / length
	# 		ratings_4[child.id] = summa
	# 	else:
	# 		ratings_4[child.id] = 0

	# 	children_list_4[child.id] = child
	
	# sorting_4 = sorted(ratings_4.items(), key=operator.itemgetter(1), reverse=True)


	# if request.POST:
	# 	filename = 'prof_master ('
	# 	if 'type_1' in request.POST:
	# 		children_list = children_list_1
	# 		sorting = sorting_1
	# 		name = 'ДШИ, ДХШ (13-14 лет)'
	# 		filename += 'dshi-13-14'
	# 	elif  'type_2' in request.POST:
	# 		children_list = children_list_2
	# 		sorting = sorting_2
	# 		name = 'ДШИ, ДХШ (от 15 лет)'
	# 		filename += 'dshi-15'
	# 	elif  'type_3' in request.POST:
	# 		children_list = children_list_3
	# 		sorting = sorting_3
	# 		name = 'Студенты СПО'
	# 		filename += 'spo'
	# 	else:
	# 		children_list = children_list_4
	# 		sorting = sorting_4
	# 		name = 'Студенты ВПО'
	# 		filename = 'vpo'
	# 	filename += ')'


	# 	dte = date.today()
	# 	document = Document()
	# 	section = document.sections[-1]
	# 	new_width, new_height = section.page_height, section.page_width
	# 	section.orientation = WD_ORIENT.PORTRAIT
	# 	section.page_width = Mm(297)
	# 	section.page_height = Mm(210)
	# 	section.left_margin = Mm(30)
	# 	section.right_margin = Mm(10)
	# 	section.top_margin = Mm(10)
	# 	section.bottom_margin = Mm(10)
	# 	section.header_distance = Mm(10)
	# 	section.footer_distance = Mm(10)

	# 	style = document.styles['Normal']
	# 	font = style.font
	# 	font.name = 'Times New Roman'
	# 	font.size = Pt(12)


	# 	document.add_paragraph('Конкурс профессионального мастерства (' + name + ')').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
	# 	p = document.add_paragraph()
	# 	p.add_run(dte.strftime('%d.%b.%Y')).italic = True
	# 	p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

	# 	table = document.add_table(rows=1, cols=6)
	# 	table.allow_autifit = False
	# 	table.style = 'TableGrid'
	# 	table.columns[0].width = Mm(10)
	# 	table.columns[1].width = Mm(22)
	# 	table.columns[2].width = Mm(65)
	# 	table.columns[3].width = Mm(65)
	# 	table.columns[4].width = Mm(65)
	# 	table.columns[5].width = Mm(20)

	# 	hdr_cells = table.rows[0].cells
	# 	hdr_cells[0].text = '№'
	# 	hdr_cells[0].width = Mm(10)
	# 	hdr_cells[1].text = 'Рег.номер'
	# 	hdr_cells[1].width = Mm(22)
	# 	hdr_cells[2].text = 'Конкурсант'
	# 	hdr_cells[2].width = Mm(65)
	# 	hdr_cells[3].text = 'Преподаватель'
	# 	hdr_cells[3].width = Mm(65)
	# 	hdr_cells[4].text = 'Учреждение'
	# 	hdr_cells[4].width = Mm(65)
	# 	hdr_cells[5].text = 'Оценка'
	# 	hdr_cells[5].width = Mm(20)


	# 	cnt = 1
	# 	for key, val in sorting:
	# 		child = children_list[key]

	# 		row_cells = table.add_row().cells
	# 		row_cells[0].text = str(cnt)
	# 		row_cells[0].width = Mm(10)
	# 		row_cells[1].text = str(child.id)
	# 		row_cells[1].width = Mm(22)
	# 		row_cells[2].text = child.get_full_name()
	# 		row_cells[2].width = Mm(65)
	# 		if child.teacher_plus_flag:
	# 			row_cells[3].text = child.teacher_plus.get_full_name()
	# 		else:
	# 			row_cells[3].text = child.teacher.profile.get_full_name()
	# 		row_cells[3].width = Mm(65)
	# 		row_cells[4].text = child.teacher.profile.institution
	# 		row_cells[4].width = Mm(65)
	# 		row_cells[5].text = str(val)
	# 		row_cells[5].width = Mm(20)

	# 		cnt += 1



	# 	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
	# 	response['Content-Disposition'] = 'attachment; filename=' + filename +' (' + dte.strftime('%d-%b-%Y') + ').docx'
	# 	document.save(response)

	# 	return response

	# args = {
	# 	'children_list_1': children_list_1, 
	# 	'children_list_2': children_list_2, 
	# 	'children_list_3': children_list_3, 
	# 	'children_list_4': children_list_4, 
	# 	'sorting_1': sorting_1,
	# 	'sorting_2': sorting_2,
	# 	'sorting_3': sorting_3,
	# 	'sorting_4': sorting_4
	# }
	# return render(request, 'ratings/view_master.html', args)

