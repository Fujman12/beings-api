# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import BeingsListEvent, BeingsEvent
from django.contrib import admin


@admin.register(BeingsListEvent)
class BeingsListEventAdmin(admin.ModelAdmin):
    list_display = ['event']


@admin.register(BeingsEvent)
class BeingsEventAdmin(admin.ModelAdmin):

    list_display = ['being', 'prev_state']