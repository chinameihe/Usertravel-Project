from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['name'].isalpha() == False:
            errors["name"] = "Name should be all characters"
            if len(postData['name']) < 3:
                errors["name"] = "Name should be at least 3 characters"

        if len(postData['username']) < 3:
            errors["username"] = "Username should be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email'] = 'Invalid Email Address'
        user = User.objects.filter(username=postData['username'])
        if(user):
            errors['username'] = 'Username is already in use'
        if postData['confirm_pw'] != postData['password']:
            errors['password'] = "Password not matching"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    travllers = models.ManyToManyField(User, related_name='trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
