from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class userManager(models.Manager):
    def validator(self, postData, register):

        errors = {}
        if register is True:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name must be at least 2 letters, dummy!"
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name must be at least 2 letters, cmon!"
            if len(postData['passwordReg']) < 8:
                errors['shortPassword'] = "Your password must be at least 8 characters!"
            if postData['passwordReg'] != postData['passwordConfirm']:
                errors['nonMatch'] = "Your passwords do not match! Try again"
            if not EMAIL_REGEX.match(postData['emailReg']):
                errors['invalidEmail'] = "Invalid, try another email"

        if register is False:
            user1 = user.objects.filter(email=postData['emailLogin'])
            
            if len(user1) is 0:
                errors['email'] = "Invalid"
            if len(postData['emailLogin']) < 2:
                errors['noEmail'] = "Invalid"
            else:
                if not bcrypt.checkpw(postData['passwordLogin'].encode(),user1[0].password.encode()):
                    errors['invalid'] = "Invalid"

        
        return errors

class user(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = userManager()

    # blog = models.ForeignKey(Blog, related_name = "comments")