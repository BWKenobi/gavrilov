import os
import datetime
import time

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import ChildForm, MasterUploadForm
from .models import Child
from pictures.models import Picture


@login_required(login_url='/login/')
def new_child(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_child = ChildForm(request.POST, label_suffix='')

		if form_child.is_valid():
			if form_child.has_changed():
				child = form_child.save(commit=False)
				child.teacher = request.user
				child.save()	

			
			return redirect('home')

		args ={
			'form': form_child, 
		}
		return render(request, 'children/new_child.html', args)

	form_child= ChildForm(admin=request.user, label_suffix='')

	args = {
		'form': form_child, 
	}
	return render(request, 'children/new_child.html', args)


@login_required(login_url='/login/')
def view_child(request, pk):
	child = Child.objects.get(pk=pk)
	if child.teacher != request.user and not request.user.profile.admin_access:
		return redirect('home')

	edit = False
	if child.teacher == request.user:
		edit = True
	
	pictures = Picture.objects.filter(author=child)
	master = False

	if request.method=='POST':
		if 'delete' in request.POST:
			child.delete()
			return redirect('home')

		if 'changeinfo' in request.POST:
			return redirect('children:edit_child', pk = child.pk)

		if 'addpict' in request.POST:
			return redirect('pictures:load_image', pk = child.pk)

		form = MasterUploadForm(request.POST, request.FILES)
		if form.is_valid():
			if form.cleaned_data['file_one']:
				if 'file_one' in request.FILES:
					child.file_one = request.FILES['file_one']
					child.save()
			if form.cleaned_data['file_two']:
				if 'file_two' in request.FILES:
					child.file_two = request.FILES['file_two']
					child.save()
			if form.cleaned_data['file_fin']:
				if 'file_fin' in request.FILES:
					child.file_fin = request.FILES['file_fin']
					child.save()
		master = True


	form = MasterUploadForm()
	args = {
		'child': child,
		'pictures': pictures,
		'edit': edit,
		'master': master,
		'form': form
	}
	return render(request, 'children/view_child.html', args)


@login_required(login_url='/login/')
def edit_child(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	child = Child.objects.get(pk=pk)
	if child.teacher != request.user:
		return redirect('home')

	if request.method=='POST':
		form_child = ChildForm(request.POST, instance=child, admin=request.user, label_suffix='')

		if form_child.is_valid():
			if form_child.has_changed():
				child = form_child.save(commit=False)
				child.save()	

			return redirect('children:view_child', pk = child.pk)

		args ={
			'form': form_profile, 
		}
		return render(request, 'children/edit_child.html', args)

	form_child= ChildForm(instance=child, admin=request.user, label_suffix='')

	args = {
		'form': form_child, 
	}
	return render(request, 'children/edit_child.html', args)
