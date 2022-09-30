import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import StatementForm
from .models import Statement


@login_required(login_url='/login/')
def new_statement(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_statement = StatementForm(request.POST, request.FILES, label_suffix='')

		if form_statement.is_valid():
			statement = form_statement.save(commit=False)
			statement.owner = request.user
			statement.save()	

			if 'file' in request.FILES:
				statement.file = request.FILES['file']
				statement.save()

			return redirect('statements:view_statement')

		args ={
			'form': form_statement, 
		}
		return render(request, 'statements/new_statement.html', args)

	form_statement = StatementForm(label_suffix='')

	args = {
		'form': form_statement, 
	}
	return render(request, 'statements/new_statement.html', args)


@login_required(login_url='/login/')
def view_statement(request):
	if not request.user.profile.member_access:
		return redirect('home')
		
	if request.method=='POST':
		return redirect('statements:new_statement')

	statements = Statement.objects.filter(owner = request.user).order_by('owner')
	args = {
		'statements': statements,
	}
	return render(request, 'statements/view_statement.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_statement(request):
	statement_pk = request.GET['statement']
	statement = Statement.objects.get(pk=statement_pk)

	if statement.owner != request.user:
		return HttpResponse(False)

	statement.delete()

	return HttpResponse(True)