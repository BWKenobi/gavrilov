import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import PictureUploadForm, PictureEditForm
from .models import Picture


@login_required(login_url='/login/')
def view_arts(request):
	pictures = Picture.objects.filter(author=request.user)

	if request.method=='POST':
		return redirect('pictures:load_image')

	args = {
		'pictures': pictures,
	}
	return render(request, 'pictures/view_arts.html', args)


@login_required(login_url='/login/')
def load_image(request):
	if not request.user.profile.member_access:
		return redirect('home')

	author = request.user


	if request.method=='POST':
		form_img = PictureUploadForm(request.POST, request.FILES, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.author = author
			new_img.save()	

			if 'file' in request.FILES:
				new_img.file = request.FILES['file']
				new_img.save()

			return redirect('pictures:view_arts')

		args = {
			'form': form_img,
		}
		return render(request, 'pictures/load_image.html', args)	
	
	form_img = PictureUploadForm(label_suffix='')

	args = {
		'form': form_img,
	}
	return render(request, 'pictures/load_image.html', args)


@login_required(login_url='/login/')
def edit_image(request, pk):
	if not request.user.profile.member_access:
		return redirect('home')
		
	pict = Picture.objects.get(pk=pk)
	author = request.user

	if pict.author != author:
		return redirect('home')

	if request.method=='POST':
		form_img = PictureEditForm(request.POST, request.FILES, instance=pict, label_suffix='')

		if form_img.is_valid():
			new_img = form_img.save(commit=False)
			new_img.author = author
			new_img.save()	

			return redirect('pictures:view_arts')

		args = {
			'form': form_img,
		}
		return render(request, 'pictures/edit_image.html', args)	
	
	form_img = PictureEditForm(instance=pict, label_suffix='')

	args = {
		'form': form_img,
		'pict': pict
	}
	return render(request, 'pictures/edit_image.html', args)

	
# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_image(request):
	image_pk = request.GET['image']
	picture = Picture.objects.get(pk=image_pk)

	if picture.author != request.user:
		return HttpResponse(False)

	picture.delete()

	return HttpResponse(True)