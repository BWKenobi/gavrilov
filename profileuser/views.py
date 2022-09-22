import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from .forms import ProfileUdpateForm, CoProfileForm

from .models import Profile, CoProfile


@login_required(login_url='/login/')
def view_edit_profile(request):
	username = request.user.username

	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix=':')

		if "passchange" in request.POST:
			return redirect('passchange')

		if form_profile.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			
			return redirect('home')

		args ={
			'form': form_profile, 
		}
		return render(request, 'profileuser/view_edit_profile.html', args)

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix=':')

	args = {
		'form': form_profile, 
	}
	return render(request, 'profileuser/view_edit_profile.html', args)


@login_required(login_url='/login/')
def view_coprofiles(request):
	if not request.user.profile.member_access:
		return redirect('home')
		
	if request.method=='POST':
		return redirect('profiles:new_coprofile')

	coprofiles = CoProfile.objects.filter(main_user = request.user).order_by('main_user')
	
	args = {
		'coprofiles': coprofiles,
	}
	return render(request, 'profileuser/view_coprofiles.html', args)


@login_required(login_url='/login/')
def new_coprofile(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_coprofile = CoProfileForm(request.POST, label_suffix='')

		if form_coprofile.is_valid():
			coprofile = form_coprofile.save(commit=False)
			coprofile.main_user = request.user
			coprofile.save()	

			return redirect('profiles:view_coprofiles')

		args ={
			'form': form_coprofile, 
		}
		return render(request, 'profileuser/new_coprofile.html', args)

	form_coprofile = CoProfileForm(label_suffix='')

	args = {
		'form': form_coprofile, 
	}
	return render(request, 'profileuser/new_coprofile.html', args)


@login_required(login_url='/login/')
def view_edit_coprofile(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')

	coprofile = CoProfile.objects.get(pk = pk)

	if request.method=='POST':
		form_coprofile = CoProfileForm(request.POST, instance=coprofile, label_suffix=':')

		if form_coprofile.is_valid():
			if form_coprofile.has_changed():
				coprofile = form_coprofile.save(False)
				coprofile.save()	

			return redirect('profiles:view_coprofiles')

		args ={
			'form': form_coprofile, 
		}
		return render(request, 'profileuser/view_edit_coprofile.html', args)

	form_coprofile = CoProfileForm(instance=coprofile, label_suffix=':')

	args = {
		'form': form_coprofile, 
	}
	return render(request, 'profileuser/view_edit_coprofile.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_coprofile(request):
	coprofile_pk = request.GET['coprofile']
	coprofile = CoProfile.objects.get(pk=coprofile_pk)

	if coprofile.main_user != request.user:
		return HttpResponse(False)

	coprofile.delete()

	return HttpResponse(True)