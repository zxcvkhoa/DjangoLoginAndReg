from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.db import models
import bcrypt, re


def index(request):
    context = {
        "user": user.objects.all(),
    }

    return render(request, "first_app/index.html", context)

def registration(request):
    
    errors = user.objects.validator(request.POST, True)
        # check if the errors object has anything in it
    if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            # redirect the user back to the form to fix the errors
        return redirect('/')

    elif len(user.objects.filter(email = request.POST['emailReg'])) > 0:
        errors['duplicate_email'] = "This Email already exists"
        messages.error(request, errors['duplicate_email'], extra_tags = "duplicate_email")
        return redirect('/')

    else:
        passHash = bcrypt.hashpw(request.POST['passwordReg'].encode(), bcrypt.gensalt())
        request.session['first_name'] = request.POST['first_name']
        b = user.objects.create()
        b.first_name = request.POST['first_name']
        b.last_name = request.POST['last_name']
        b.email = request.POST['emailReg']
        b.password = passHash
        b.save()

        return redirect('/success')

def login(request):
    if request.method == "POST":
        errors = user.objects.validator(request.POST, False)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        else:
            currentUser = user.objects.get(email = request.POST['emailLogin'])
            request.session['first_name'] = currentUser.first_name
            request.session['id'] = currentUser.id
            return redirect('/success')
            


def success(request):
    context = {
        "user": user.objects.all(),
    }
    return render(request, "first_app/success.html", context)

def logout(request):
    request.session.clear()

    return redirect('/')