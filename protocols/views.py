import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import ProtocolForm
from .models import Protocol


@login_required(login_url='/login/')
def new_protocol(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_protocol = ProtocolForm(request.POST, request.FILES, label_suffix='')

		if form_protocol.is_valid():
			protocol = form_protocol.save(commit=False)
			protocol.owner = request.user
			protocol.save()	

			if 'file' in request.FILES:
				protocol.file = request.FILES['file']
				protocol.save()

			return redirect('protocols:view_protocol')

		args ={
			'form': form_invoice, 
		}
		return render(request, 'protocols/new_protocol.html', args)

	form_protocol = ProtocolForm(label_suffix='')

	args = {
		'form': form_protocol, 
	}
	return render(request, 'protocols/new_protocol.html', args)


@login_required(login_url='/login/')
def view_protocol(request):
	if not request.user.profile.member_access:
		return redirect('home')
		
	if request.method=='POST':
		return redirect('protocols:new_protocol')

	protocols = Protocol.objects.filter(owner = request.user).order_by('owner')
	args = {
		'protocols': protocols,
	}
	return render(request, 'protocols/view_protocol.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_protocol(request):
	protocol_pk = request.GET['protocol']
	protocol = Protocol.objects.get(pk=protocol_pk)

	if protocol.owner != request.user:
		return HttpResponse(False)

	protocol.delete()

	return HttpResponse(True)