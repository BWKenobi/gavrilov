import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import InvoiceForm
from .models import Invoice


@login_required(login_url='/login/')
def new_invoice(request):
	if not request.user.profile.member_access:
		return redirect('home')

	if request.method=='POST':
		form_invoice = InvoiceForm(request.POST, request.FILES, label_suffix='')

		if form_invoice.is_valid():
			invoice = form_invoice.save(commit=False)
			invoice.payer = request.user
			invoice.save()	

			if 'file' in request.FILES:
				invoice.file = request.FILES['file']
				invoice.save()

			return redirect('invoices:view_invoice')

		args ={
			'form': form_invoice, 
		}
		return render(request, 'invoices/new_invoice.html', args)

	form_invoice= InvoiceForm(label_suffix='')

	args = {
		'form': form_invoice, 
	}
	return render(request, 'invoices/new_invoice.html', args)


@login_required(login_url='/login/')
def view_invoice(request):
	if not request.user.profile.member_access:
		return redirect('home')
		
	if request.method=='POST':
		return redirect('invoices:new_invoice')

	invoices = Invoice.objects.filter(payer = request.user).order_by('date')
	args = {
		'invoices': invoices,
	}
	return render(request, 'invoices/view_invoice.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_invoice(request):
	invoice_pk = request.GET['invoice']
	invoice = Invoice.objects.get(pk=invoice_pk)

	if invoice.payer != request.user:
		return HttpResponse(False)

	invoice.delete()

	return HttpResponse(True)