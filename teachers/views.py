import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import TeacherForm
from .models import Teacher


@login_required(login_url='/login/')
def new_teacher(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_teacher = TeacherForm(request.POST, label_suffix='')

		if form_teacher.is_valid():
			if form_teacher.has_changed():
				teacher = form_teacher.save(commit=False)
				teacher.host_accaunt = request.user
				teacher.save()	

			
			return redirect('home')

		args ={
			'form': form_teacher, 
		}
		return render(request, 'teachers/new_teacher.html', args)

	form_teacher= TeacherForm(label_suffix='')

	args = {
		'form': form_teacher, 
	}
	return render(request, 'teachers/new_teacher.html', args)


@login_required(login_url='/login/')
def view_teacher(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')

	teacher = Teacher.objects.get(pk=pk)
	if teacher.host_accaunt != request.user:
		return redirect('home')
	
	if request.method=='POST':
		if 'delete' in request.POST:
			teacher.delete()
			return redirect('home')

		if 'changeinfo' in request.POST:
			return redirect('teachers:edit_teacher', pk = teacher.pk)


	args = {
		'teacher': teacher,
	}
	return render(request, 'teachers/view_teacher.html', args)


@login_required(login_url='/login/')
def edit_teacher(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	teacher = Teacher.objects.get(pk=pk)
	if teacher.host_accaunt != request.user:
		return redirect('home')

	if request.method=='POST':
		form_teacher = TeacherForm(request.POST, instance=teacher, label_suffix='')

		if form_teacher.is_valid():
			if form_teacher.has_changed():
				teacher = form_teacher.save(commit=False)
				teacher.save()	

			return redirect('teachers:view_teacher', pk = teacher.pk)

		args ={
			'form': form_teacher, 
		}
		return render(request, 'teachers/edit_teacher.html', args)

	form_teacher= TeacherForm(instance=teacher, label_suffix='')

	args = {
		'form': form_teacher, 
	}
	return render(request, 'teachers/edit_teacher.html', args)

