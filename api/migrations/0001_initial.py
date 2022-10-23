# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-10-23 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=1000)),
                ('key', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('breed', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('color', models.CharField(max_length=100)),
                ('favoritefood', models.CharField(max_length=100)),
                ('favortietoy', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventtype', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField()),
                ('userid', models.CharField(blank=True, max_length=1000)),
                ('requestor', models.GenericIPAddressField()),
            ],
        ),
    ]
