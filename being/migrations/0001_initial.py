# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 10:51
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Being',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Being name')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('state', models.CharField(choices=[('new', 'new'), ('happy', 'happy'), ('sad', 'sad')], default='new', max_length=10, verbose_name='State')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Being',
                'verbose_name_plural': 'Beings',
            },
        ),
    ]
