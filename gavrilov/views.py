import os
import time
from django.db.models import Q
from datetime import date
import json
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.shared import Mm, Pt

from fpdf import FPDF

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

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from .tokens import accaunt_activation_token

from profileuser.models import Profile
from children.models import Child
from pictures.models import Picture
from invoices.models import Invoice
from certificates.models import Certificate
from children.forms import GroupForm
from .forms import UserLoginForm, UserRegistrationForm, ChangePasswordForm, CustomPasswordResetForm, CustomSetPasswordForm
from .forms import SetJuriForm, ChangeJuriForm, NewJuriForm

class PDF(FPDF):
	pass

def home_view(request):
	certificates = None

	if request.user.is_authenticated:
		user = request.user
		children = Child.objects.filter(teacher=user)
		certificates = Certificate.objects.filter(child__in = children)

	args = {
		'certificates': certificates
	}
	return render(request, 'index.html', args)


def policy_view(request):
	return render(request, 'policy.html')


def login_view(request):
	form = UserLoginForm(request.POST or None)
	next_ = request.GET.get('next')
	modal = False

	if form.is_valid():
		username = request.POST.get('email').lower()
		password = request.POST.get('password')
		user = authenticate(username = username.strip(), password = password.strip())
		
		login(request, user)
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or '/'


		return redirect(redirect_path)

	args = {
		'form': form
	}
	return render(request, 'login.html', args)


def logout_view(request):
	logout(request)
	return redirect('home')


def register_view(request):
	if request.method=='POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.username = new_user.email
			new_user.is_active = False
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()

			new_user.profile.name = user_form.cleaned_data['name']
			new_user.profile.name2 = user_form.cleaned_data['name2']
			new_user.profile.surname = user_form.cleaned_data['surname']
			new_user.profile.institution = user_form.cleaned_data['institution']
			new_user.profile.adress = user_form.cleaned_data['adress']
			new_user.profile.surname_director = user_form.cleaned_data['surname_director']
			new_user.profile.name_director = user_form.cleaned_data['name_director']
			new_user.profile.name_director2 = user_form.cleaned_data['name_director2']
			new_user.profile.save()

			current_site = get_current_site(request)
			protocol = 'http'
			if request.is_secure():
				protocol = 'https'

			mail_subject = 'Активация аккаунта'
			to_email = new_user.email
			#if '127.0.0.1' in current_site.domain:
			uid = urlsafe_base64_encode(force_bytes(new_user.pk))
			#else:
			#	uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()

			token = accaunt_activation_token.make_token(new_user)

			message = render_to_string('acc_active_email.html', {'user': new_user, 'domain': current_site.domain,\
				'uid': uid, \
				'token': token,\
				'protocol': protocol,\
				'email': to_email})

			message_html = render_to_string('acc_active_email_html.html', {'user': new_user, 'domain': current_site.domain,\
				'uid': uid, \
				'token': token,\
				'protocol': protocol,\
				'email': to_email})

			send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

			return render(request, 'confirm_email.html')

		return render(request, 'register.html', {'form': user_form})

	user_form = UserRegistrationForm()
	return render(request, 'register.html', {'form': user_form})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user and accaunt_activation_token.check_token(user, token):
		user.is_active = True
		user.save()

		login(request, user)
		return redirect('home')

	return render(request, 'failed_email.html')


def change_password(request):
	username = request.user.username

	if request.method == 'POST':
		form = ChangePasswordForm(request.POST, username=username)

		if form.is_valid():
			user = request.user
			user.set_password(form.cleaned_data['newpassword1'])
			user.save()
			update_session_auth_hash(request, user)

			return redirect('profiles:view_edit_profile')

		args = {
			'form': form
		}
		return render(request, 'change_password.html', args)

	form = ChangePasswordForm(username=username)

	args = {
		'form': form
	}
	return render(request, 'change_password.html', args)


@login_required(login_url='/login/')
def statistic_children_view(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	children = Child.objects.all().order_by('surname', 'name', 'name2')
	pictures = Picture.objects.all()
	array = {}
	for child in children:
		picts = pictures.filter(author=child)
		if picts:
			array[child.id] = len(picts)
		else:
			array[child.id] = 0

	groups = {}
	for child in children:
		groups[child.pk] = GroupForm(instance=child)

	if request.POST:
		if 'saving' in request.POST:
			cnt = 0
			grs = request.POST.getlist('group')
			for child in children:
				child.group = grs[cnt]
				child.save()
				cnt += 1

				groups[child.pk] = GroupForm(instance=child)
		else:
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


			document.add_paragraph('Список участников конкурса').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
			p = document.add_paragraph()
			p.add_run(dte.strftime('%d.%b.%Y')).italic = True
			p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

			table = document.add_table(rows=1, cols=7)
			table.allow_autifit = False
			table.style = 'TableGrid'
			table.columns[0].width = Mm(10)
			table.columns[1].width = Mm(50)
			table.columns[2].width = Mm(50)
			table.columns[3].width = Mm(50)
			table.columns[4].width = Mm(30)
			table.columns[5].width = Mm(30)
			table.columns[6].width = Mm(37)

			hdr_cells = table.rows[0].cells
			hdr_cells[0].text = '№'
			hdr_cells[0].width = Mm(10)
			hdr_cells[1].text = 'Конкурсант'
			hdr_cells[1].width = Mm(50)
			hdr_cells[2].text = 'Преподаватель'
			hdr_cells[2].width = Mm(50)
			hdr_cells[3].text = 'Учреждение'
			hdr_cells[3].width = Mm(50)
			hdr_cells[4].text = 'Врзрастная группа'
			hdr_cells[4].width = Mm(30)
			hdr_cells[5].text = 'Кол-во работ'
			hdr_cells[5].width = Mm(30)
			hdr_cells[6].text = 'Участие в кокурсе профессионального мастерства'
			hdr_cells[6].width = Mm(37)

			for child in children:
				row_cells = table.add_row().cells
				row_cells[0].text = str(child.id)
				row_cells[0].width = Mm(10)
				row_cells[1].text = child.get_full_name()
				row_cells[1].width = Mm(50)
				if child.teacher_plus:
					row_cells[2].text = child.teacher_plus.get_full_name()
				else:
					row_cells[2].text =child.teacher.profile.get_full_name()
				row_cells[2].width = Mm(50)
				row_cells[3].text = child.teacher.profile.institution
				row_cells[3].width = Mm(50)
				if child.group:
					row_cells[4].text = child.get_group_display()
				else:
					row_cells[4].text = "-"
				row_cells[4].width = Mm(30)
				row_cells[5].text = str(array[child.id])
				row_cells[5].width = Mm(30)
				if child.master_flag:
					row_cells[6].text = '+'
				else:
					row_cells[6].text = '-'
				row_cells[6].width = Mm(37)



			response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = 'attachment; filename=List (' + dte.strftime('%d-%b-%Y') + ').docx'
			document.save(response)

			return response

	args = {
		'children': children,
		'array': array,
		'groups': groups
	}
	return render(request, 'statistic_children.html', args)


@login_required(login_url='/login/')
def statistic_invoices_view(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	profiles = Profile.objects.filter(member_access=True).exclude(user__username='admin').exclude(user__is_active=False).order_by('surname', 'name', 'name2')
	invoices = Invoice.objects.all()
	array = {}
	array_sum = {}
	for profile in profiles:
		inces = invoices.filter(payer=profile.user)
		if inces:
			summa = 0
			array[profile.id] = inces
			for ince in inces:
				summa += ince.summa
			array_sum[profile.id] = summa


	if request.POST:
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


		document.add_paragraph('Список оплат').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		table = document.add_table(rows=1, cols=5)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(70)
		table.columns[2].width = Mm(70)
		table.columns[3].width = Mm(30)
		table.columns[4].width = Mm(77)


		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'Куратор'
		hdr_cells[1].width = Mm(70)
		hdr_cells[2].text = 'Учреждение'
		hdr_cells[2].width = Mm(70)
		hdr_cells[3].text = 'Оплаченная сумма'
		hdr_cells[3].width = Mm(30)
		hdr_cells[4].text = 'Квитанции'
		hdr_cells[4].width = Mm(77)

		cnt = 1
		for profile in profiles:
			row_cells = table.add_row().cells
			row_cells[0].text = str(cnt)
			row_cells[0].width = Mm(10)
			row_cells[1].text = profile.get_full_name()
			row_cells[1].width = Mm(70)
			row_cells[2].text = profile.institution
			row_cells[2].width = Mm(70)
			row_cells[3].text = '0'
			if profile.id in array_sum:
				row_cells[3].text = str(array_sum[profile.id])
			row_cells[3].width = Mm(30)
			row_cells[4].text = ''
			if profile.id in array:
				for invoice in array[profile.id]:
					row_cells[4].text += 'Дата: ' + str(invoice.date) + ', сумма: ' + str(invoice.summa) + ' руб.\n'
			row_cells[4].width = Mm(77)

			cnt += 1



		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=InvoiceList (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'profiles': profiles,
		'array': array,
		'array_sum': array_sum
	}
	return render(request, 'statistic_invoices.html', args)

	
@login_required(login_url='/login/')
def statistic_institution_view(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	profiles = Profile.objects.filter(member_access=True).exclude(user__username='admin').exclude(user__is_active=False).order_by('surname', 'name', 'name2')
	chilren = Child.objects.all()
	invoices = Invoice.objects.all()
	pictures = Picture.objects.all()

	array = {}
	array_sum = {}
	array_cnt = {}
	array_works = {}
	for profile in profiles:
		sum_work = 0
		chlds = chilren.filter(teacher=profile.user)
		inces = invoices.filter(payer=profile.user)
		if chlds:
			array[profile.id] = chlds
			if inces:
				summa = 0
				for ince in inces:
					summa += ince.summa
				array_sum[profile.id] = summa

			for chld in chlds:
				picts = pictures.filter(author=chld)
				if picts:
					array_cnt[chld.id] = len(picts)
					sum_work += len(picts)
				else:
					array_cnt[chld.id] = 0

				if chld.master_flag:
					sum_work += 1

		array_works[profile.id] = sum_work


	if request.POST:
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


		document.add_paragraph('Список по учреждениям').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		for profile in profiles:
			p = document.add_paragraph()
			pp = p.add_run(profile.institution)
			pp.font.size = Pt(14)
			pp.bold = True
			p.paragraph_format.space_after = 0

			p = document.add_paragraph()
			p.add_run('Куратор: ').bold = True
			p.add_run(profile.get_full_name())
			p.add_run(' (' +  profile.user.email + ')').italic = True
			p.paragraph_format.space_after = 0
			
			p = document.add_paragraph()
			p.add_run('Оплаченная сумма: ').bold = True
			try:
				p.add_run(str(array_sum[profile.id]) + ' руб.')
				p.paragraph_format.space_after = 0
			except:
				p.add_run('0 руб.')
				p.paragraph_format.space_after = 0

			p = document.add_paragraph()
			p.add_run('Всего едениц участия: ').bold = True	
			p.add_run(str(array_works[profile.pk]))
			p.paragraph_format.space_after = 0


			table = document.add_table(rows=1, cols=5)
			table.allow_autifit = False
			table.style = 'TableGrid'
			table.columns[0].width = Mm(10)
			table.columns[1].width = Mm(90)
			table.columns[2].width = Mm(90)
			table.columns[3].width = Mm(30)
			table.columns[4].width = Mm(37)


			hdr_cells = table.rows[0].cells
			hdr_cells[0].text = '№'
			hdr_cells[0].width = Mm(10)
			hdr_cells[1].text = 'Конкурсант'
			hdr_cells[1].width = Mm(90)
			hdr_cells[2].text = 'Преподаватель'
			hdr_cells[2].width = Mm(90)
			hdr_cells[3].text = 'Количество работ'
			hdr_cells[3].width = Mm(30)
			hdr_cells[4].text = 'Участие в кокурсе профессионального мастерств'
			hdr_cells[4].width = Mm(37)

			cnt = 1
			try:
				for child in array[profile.id]:
					row_cells = table.add_row().cells
					row_cells[0].text = str(cnt)
					row_cells[0].width = Mm(10)
					row_cells[1].text = child.get_full_name()
					row_cells[1].width = Mm(90)
					if child.teacher_plus:
						row_cells[2].text = child.teacher_plus.get_full_name()
					else:
						row_cells[2].text = child.teacher.profile.get_full_name()
					row_cells[2].width = Mm(90)
					row_cells[3].text = '0'
					row_cells[3].text = str(array_cnt[child.id])
					row_cells[3].width = Mm(30)
					if child.master_flag:
						t = row_cells[4]
						t.text = 'Участвует'
						t.paragraphs[0].runs[0].bold = True
					else:
						row_cells[4].text = 'Не участвует'
					row_cells[4].width = Mm(37)

					cnt += 1
			except:
				pass

			document.add_paragraph().paragraph_format.space_after = 0
			document.add_paragraph().paragraph_format.space_after = 0

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=InstitutionsList (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'profiles': profiles,
		'array': array,
		'array_sum': array_sum,
		'array_cnt': array_cnt,
		'array_works': array_works
	}
	return render(request, 'statistic_institution.html', args)


@login_required(login_url='/login/')
def juri_view(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	chef_juris = Profile.objects.filter(chef_juri_accecc=True) 
	juris = Profile.objects.filter(juri_accecc=True).exclude(chef_juri_accecc=True)


	if request.method=='POST':
		if 'new' in request.POST:
			return redirect('juri_new')

		return redirect('juri_set')

	args = {
		'chef_juris': chef_juris,
		'juris': juris,
	}
	return render(request, 'view_juri.html', args)


@login_required(login_url='/login/')
def juri_set(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	pretendents = Profile.objects.filter(user__is_active=True).exclude(user__username='admin').exclude(juri_accecc=True).exclude(chef_juri_accecc=True).order_by('surname', 'name', 'name2')

	if request.POST:
		form = SetJuriForm(request.POST, pretendents=pretendents)	
		if form.is_valid():
			pretendent = form.cleaned_data['juri']
			pretendent.juri_accecc = True
			pretendent.chef_juri_accecc = form.cleaned_data['chef']
			pretendent.save()

			return redirect('juri_view')

	form = SetJuriForm(pretendents=pretendents)
	args = {
		'form': form
	}
	return render(request, 'juri_set.html', args)


@login_required(login_url='/login/')
def juri_change(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	pretendent = Profile.objects.get(pk = pk)

	if request.POST:
		form = ChangeJuriForm(request.POST, instance=pretendent)	
		if form.is_valid():
			pretendent = form.save(commit=False)
			pretendent.save()

			return redirect('juri_view')

	form = ChangeJuriForm(instance=pretendent)
	args = {
		'pretendent': pretendent,
		'form': form
	}
	return render(request, 'juri_change.html', args)


@login_required(login_url='/login/')
def juri_new(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	if request.method=='POST':
		form = NewJuriForm(request.POST)
		if form.is_valid():
			password = User.objects.make_random_password(8)
			new_user = form.save(commit=False)
			new_user.username = new_user.email
			new_user.is_active = True
			new_user.set_password(password)
			new_user.save()

			new_user.profile.name = form.cleaned_data['name']
			new_user.profile.name2 = form.cleaned_data['name2']
			new_user.profile.surname = form.cleaned_data['surname']
			new_user.profile.institution = form.cleaned_data['institution']
			new_user.profile.adress = form.cleaned_data['adress']
			new_user.profile.rank = form.cleaned_data['rank']
			new_user.profile.member_access = False
			new_user.profile.juri_accecc = True
			new_user.profile.chef_juri_accecc = form.cleaned_data['chef_juri_accecc']
			new_user.profile.save()

			protocol = 'http'
			if request.is_secure():
				protocol = 'https'
			current_site = get_current_site(request)

			mail_subject = 'Конкурс "История глазами молодых"'
			to_email = new_user.email
			sex = new_user.profile.sex()
			sex_valid = new_user.profile.sex_valid()
			signature = 'С уважением,\r\nАдминистрация конкурса'
			sign = signature.split('\r\n')

			args = {
				'sex': sex,
				'sex_valid': sex_valid,
				'name': new_user.profile.get_io_name(),
				'protocol': protocol,
				'domain': current_site.domain,
				'signature': signature,
				'sign': sign,
				'email': to_email,
				'password': password,
				'chef': new_user.profile.chef_juri_accecc
			}
				
			message = render_to_string('juri_active_email.html', args)

			message_html = render_to_string('juri_active_email_html.html', args)

			send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

			return redirect('juri_view')

		args = {
			'form': form
		}
		return render(request, 'juri_new.html', args)

	form = NewJuriForm()
	args = {
		'form': form
	}
	return render(request, 'juri_new.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def delete_juri(request):
	juri_pk = request.GET['juri']
	juri = Profile.objects.get(pk=juri_pk)

	juri.juri_accecc = False
	juri.chef_juri_accecc = False
	juri.save()

	return HttpResponse(True)