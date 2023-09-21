import os
import datetime
import locale

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Mm, Pt

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from .forms import PictureUploadForm, PictureEditForm
from profileuser.models import Profile, CoProfile
from .models import Picture, CoPicturee
from profileuser.models import CoProfile
from nominations.models import ArtNomination

@login_required(login_url='/login/')
def view_arts(request):
	pictures = Picture.objects.filter(author__main_user=request.user)
	copictures_list = {}
	for picture in pictures:
		copictures_list[picture.pk] = CoPicturee.objects.filter(picture = picture)


	if request.method=='POST':
		if 'addpict' in request.POST:
			return redirect('pictures:load_image')

		locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

		dte = date.today()

		document = Document()

		section = document.sections[-1]
		new_width, new_height = section.page_height, section.page_width
		section.orientation = WD_ORIENT.PORTRAIT
		section.page_width = Mm(210)
		section.page_height = Mm(297)
		section.left_margin = Mm(20)
		section.right_margin = Mm(10)
		section.top_margin = Mm(10)
		section.bottom_margin = Mm(10)
		section.header_distance = Mm(10)
		section.footer_distance = Mm(10)

		style = document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(14)


		p = document.add_paragraph()
		p.add_run('ЗАЯВКА').bold = True
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER

		p = document.add_paragraph()
		p.add_run('на участие во Всероссийском фестивале-конкурсе').bold = True
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER

		p = document.add_paragraph()
		p.add_run('народного творчества «Гавриловские гуляния»').bold = True
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER

		p = document.add_paragraph()
		p.add_run('(выставочная программа)').bold = True
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER

		p = document.add_paragraph()
		p.add_run(dte.strftime('%d %B %Y') + ' года').italic = True
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		document.add_paragraph().paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('1. Название направляющей организации (в соответствии с ЕГРЮЛ полное и сокращенное название): ' + request.user.profile.get_institute_full())
		if not request.user.profile.less_institution:
			p.add_run(' (' + request.user.profile.get_institute() + ')')
		p.paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('2. Почтовый адрес и индекс направляющей организации: ')
		if not request.user.profile.less_institution:
			p.add_run(request.user.profile.adress)
		p.paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('3. ФИО ответственного лица: ' + request.user.profile.get_full_name())
		p.paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('4. Телефон: ' + request.user.profile.phone)
		p.paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('5. E-mail: ' + request.user.email)
		p.paragraph_format.space_after = 0

		document.add_paragraph().paragraph_format.space_after = 0

		table = document.add_table(rows=1, cols=4)
		table.allow_autifit = False
		table.style = 'Table Grid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(45)
		table.columns[2].width = Mm(65)
		table.columns[3].width = Mm(60)


		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].paragraphs[0].runs[0].font.bold = True
		hdr_cells[0].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Номинация'
		hdr_cells[1].paragraphs[0].runs[0].font.bold = True
		hdr_cells[1].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[1].width = Mm(45)
		hdr_cells[2].text = 'Ф.И.О автора, возраст (Ф.И.О. преподавателя)'
		hdr_cells[2].paragraphs[0].runs[0].font.bold = True
		hdr_cells[2].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[2].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[2].width = Mm(65)
		hdr_cells[3].text = 'Название работы, год исполнения, техника исполнения'
		hdr_cells[3].paragraphs[0].runs[0].font.bold = True
		hdr_cells[3].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[3].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[3].width = Mm(60)

		cnt = 1
		for picture in pictures:
			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].paragraphs[0].runs[0].font.bold = True
			row_cells[0].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
			row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[0].width = Mm(10)


			row_cells[1].text = str(picture.nomination)
			row_cells[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[1].width = Mm(45)


			year = str(picture.ages) + ' ' + picture.ages_prefix()

			text = picture.author.get_full_name() + ', ' + year
			if copictures_list[picture.pk]:
				for copicture in copictures_list[picture.pk]:
					text += '\n' + copicture.coauthor.short_profile_type() + ' ' + copicture.coauthor.get_file_name()
			row_cells[2].text = text
			row_cells[2].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[2].width = Mm(65)

			text = picture.name
			if picture.technique:
				text += ',\n' + str(picture.year) + ' год,\n' + picture.technique

			row_cells[3].text = text
			row_cells[3].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[3].width = Mm(45)

			cnt += 1

		document.add_paragraph().paragraph_format.space_after = 0

		p = document.add_paragraph()
		rinner = p.add_run('Итого:')
		rinner.bold = True
		rinner.underline = True
		p.paragraph_format.space_after = 0

		nominations = ArtNomination.objects.all()

		for nomination in nominations:
			cnt = pictures.filter(nomination = nomination).count()
			if cnt:
				p = document.add_paragraph()
				p.add_run(str(nomination) + ': ')
				p.add_run(str(cnt)).underline = True

				mod = cnt % 10
				mod_plus = (cnt // 10) % 10
				if mod_plus != 1:
					if mod == 0:
						p.add_run(' работ')
					elif mod == 1:
						p.add_run(' работа')
					elif mod < 5:
						p.add_run(' работы')
				else:
					p.add_run(' работ')
				p.paragraph_format.space_after = 0

		document.add_paragraph().paragraph_format.space_after = 0

		cnt = pictures.all().count()

		p = document.add_paragraph()
		p.add_run('Всего: ').bold = True
		rinner = p.add_run(str(cnt))
		rinner.bold = True
		rinner.underline = True
		mod = cnt % 10
		mod_plus = (cnt // 10) % 10
		if mod_plus != 1:
			if mod == 0:
				p.add_run(' работ').bold = True
			elif mod == 1:
				p.add_run(' работа').bold = True
			elif mod < 5:
				p.add_run(' работы').bold = True
		else:
			p.add_run(' работ').bold = True
		p.paragraph_format.space_after = 0

		document.add_paragraph().paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('Подпись ответственного лица: _________________________________________')
		p.paragraph_format.space_after = 0

		document.add_paragraph().paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('Дата: «_______» _______________ ' + str(dte.year) + ' г.')
		p.paragraph_format.space_after = 0

		document.add_paragraph().paragraph_format.space_after = 0

		p = document.add_paragraph()
		p.add_run('Печать')
		p.paragraph_format.space_after = 0
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		file_name = 'Statement-art'
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=' + file_name +' (' + dte.strftime('%d-%m-%Y') + ').docx'
		document.save(response)

		return response


	args = {
		'pictures': pictures,
		'copictures_list': copictures_list
	}
	return render(request, 'pictures/view_arts.html', args)


@login_required(login_url='/login/')
def load_image(request):
	if not request.user.profile.member_access:
		return redirect('home')

	author = request.user
	coprofiles = CoProfile.objects.filter(main_user = author, profile_type__in = ['1', '2', '3', '4', '5'])

	if request.method=='POST':
		
		form_img = PictureUploadForm(request.POST, request.FILES, author = author, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoPicturee.objects.filter(picture = new_img, coauthor = coprofile):
						CoPicturee.objects.create(picture = new_img, coauthor = coprofile)
				else:
					CoPicturee.objects.filter(picture = new_img, coauthor = coprofile).delete()

			return redirect('pictures:view_arts')

		args = {
			'form': form_img,
			'coprofiles': coprofiles		}
		return render(request, 'pictures/load_image.html', args)	
	
	form_img = PictureUploadForm(author = author, label_suffix='')

	args = {
		'form': form_img,
		'coprofiles': coprofiles	}
	return render(request, 'pictures/load_image.html', args)



@login_required(login_url='/login/')
def load_image_admin(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	author = Profile.objects.get(pk = pk).user
	coprofiles = CoProfile.objects.filter(main_user = author)

	if request.method=='POST':
		
		if author.profile.participation == '2':
			form_img = PictureUploadForm(request.POST, request.FILES, label_suffix='')
		else:
			form_img = PictureUploadNoneFileForm(request.POST, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.author = author
			new_img.save()	
			
			if author.profile.participation == '2':
				if 'file' in request.FILES:
					new_img.file = request.FILES['file']
					new_img.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoPicturee.objects.filter(picture = new_img, coauthor = coprofile):
						CoPicturee.objects.create(picture = new_img, coauthor = coprofile)
				else:
					CoPicturee.objects.filter(picture = new_img, coauthor = coprofile).delete()

			return redirect('view_contestant', pk = author.profile.pk)

		args = {
			'form': form_img,
			'coprofiles': coprofiles,
			'author': author
		}
		return render(request, 'pictures/load_image.html', args)	
	
	if author.profile.participation == '2':
		form_img = PictureUploadForm(label_suffix='')
	else:
		form_img = PictureUploadNoneFileForm(label_suffix='')


	args = {
		'form': form_img,
		'coprofiles': coprofiles,
		'author': author
	}
	return render(request, 'pictures/load_image.html', args)


@login_required(login_url='/login/')
def edit_image(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	pict = Picture.objects.get(pk=pk)
	author = request.user
	coprofiles = CoProfile.objects.filter(main_user = author, profile_type__in = ['1', '2', '3', '4', '5'])
	copictures_list = {}

	if pict.author.main_user != author:
		return redirect('home')

	if request.method=='POST':
		form_img = PictureEditForm(request.POST, request.FILES, instance=pict, author = author, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoPicturee.objects.filter(picture = new_img, coauthor = coprofile):
						CoPicturee.objects.create(picture = new_img, coauthor = coprofile)
				else:
					CoPicturee.objects.filter(picture = new_img, coauthor = coprofile).delete()


			return redirect('pictures:view_arts')

		args = {
			'form': form_img,
		}
		return render(request, 'pictures/edit_image.html', args)	
	
	form_img = PictureEditForm(instance=pict, author = author, label_suffix='')
	copicture = list(CoPicturee.objects.filter(picture = pict).values_list('coauthor', flat=True))
	for coprofile in coprofiles:
		copictures_list[coprofile.pk] = coprofile.pk in copicture

	args = {
		'form': form_img,
		'pict': pict,
		'coprofiles': coprofiles,
		'copictures_list': copictures_list
	}
	return render(request, 'pictures/edit_image.html', args)



@login_required(login_url='/login/')
def edit_image_admin(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')
		
	pict = Picture.objects.get(pk=pk)
	author = pict.author
	coprofiles = CoProfile.objects.filter(main_user = author)
	copictures_list = {}

	if pict.author != author:
		return redirect('home')

	if request.method=='POST':
		form_img = PictureEditForm(request.POST, request.FILES, instance=pict, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.author = author
			new_img.save()

			for coprofile in coprofiles:
				test_str = 'coprofile-check-' + str(coprofile.pk)
				if test_str in request.POST:
					if not CoPicturee.objects.filter(picture = new_img, coauthor = coprofile):
						CoPicturee.objects.create(picture = new_img, coauthor = coprofile)
				else:
					CoPicturee.objects.filter(picture = new_img, coauthor = coprofile).delete()


			return redirect('view_contestant', pk = author.profile.pk)

		args = {
			'form': form_img,
		}
		return render(request, 'pictures/edit_image.html', args)	
	
	form_img = PictureEditForm(instance=pict, label_suffix='')
	copicture = list(CoPicturee.objects.filter(picture = pict).values_list('coauthor', flat=True))
	for coprofile in coprofiles:
		copictures_list[coprofile.pk] = coprofile.pk in copicture

	args = {
		'form': form_img,
		'pict': pict,
		'coprofiles': coprofiles,
		'copictures_list': copictures_list
	}
	return render(request, 'pictures/edit_image.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_image(request):
	image_pk = request.GET['image']
	picture = Picture.objects.get(pk=image_pk)

	if not request.user.profile.admin_access and picture.author.main_user != request.user:
		return HttpResponse(False)

	picture.delete()

	return HttpResponse(True)
