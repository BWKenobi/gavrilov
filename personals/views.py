import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import PersonalForm
from .models import Personal


@login_required(login_url='/login/')
def new_personal(request):
    if not request.user.profile.member_access:
        return redirect('home')

    if request.method=='POST':
        form_personal = PersonalForm(request.POST, request.FILES, label_suffix='')

        if form_personal.is_valid():
            personal = form_personal.save(commit=False)
            personal.owner = request.user
            personal.save()

            if 'file' in request.FILES:
                personal.file = request.FILES['file']
                personal.save()

            return redirect('personals:view_personal')

        args ={
            'form': form_personal,
        }
        return render(request, 'personals/new_personal.html', args)

    form_personal = PersonalForm(label_suffix='')

    args = {
        'form': form_personal,
    }
    return render(request, 'personals/new_personal.html', args)


@login_required(login_url='/login/')
def view_personal(request):
    if not request.user.profile.member_access:
        return redirect('home')

    if request.method=='POST':
        return redirect('personals:new_personal')

    personals = Personal.objects.filter(owner = request.user).order_by('owner')
    args = {
        'personals': personals,
    }
    return render(request, 'personals/view_personal.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
@login_required(login_url='/login/')
def ajax_del_personal(request):
    personal_pk = request.GET['personal']
    personal = Personal.objects.get(pk=personal_pk)

    if personal.owner != request.user:
        return HttpResponse(False)

    personal.delete()

    return HttpResponse(True)
