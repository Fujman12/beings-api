# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from autoslug import AutoSlugField


class Being(models.Model):
    STATE = (
        ('new', u'new'),
        ('happy', u'happy'),
        ('sad', u'sad'),
    )

    name = models.CharField(u'Being name',  max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, editable=True)
    created = models.DateTimeField(u'Created', auto_now_add=True, blank=True)
    state = models.CharField(u'State', max_length=10, choices=STATE, default='new')

    class Meta:
        verbose_name = u'Being'
        verbose_name_plural = u'Beings'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/being/%i/" % self.id
