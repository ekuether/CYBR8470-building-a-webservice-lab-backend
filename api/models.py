from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
import base64

class Event(models.Model):
    eventtype = models.CharField(max_length=1000, blank=False)
    timestamp = models.DateTimeField()
    userid = models.CharField(max_length=1000, blank=True)
    requestor = models.GenericIPAddressField(blank=False)

    def __str__(self):
        return str(self.eventtype)

class EventAdmin(admin.ModelAdmin):
    list_display = ('eventtype', 'timestamp')

class ApiKey(models.Model):
    owner = models.CharField(max_length=1000, blank=False)
    key = models.CharField(max_length=5000, blank=False)

    def __str__(self):
        return str(self.owner) + str(self.key)

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner','key')

class Dog(models.Model):
    name = models.CharField(max_length=100, blank=False)
    age = models.IntegerField()
    breed = models.CharField(max_length=100, blank=False)
    gender = models.CharField(max_length=1)
    color = models.CharField(max_length=100)
    favoritefood = models.CharField(max_length=100)
    favortietoy = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name) + str(self.breed)

class Breed(models.Model):
    name = models.CharField(max_length=100, blank=False)
    size = models.CharField(max_length=1,choices=[('T','Tiny'),('S','Small'),('M','Medium'),('L','Large')])
    friendliness = models.IntegerField()
    trainability = models.IntegerField()
    sheddingamount = models.IntegerField()
    exerciseneeds = models.IntegerField()

    def __str__(self):
        return str(self.name)