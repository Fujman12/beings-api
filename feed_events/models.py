# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from .utils import ping_hub
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from being.models import Being
from django.db.models.signals import post_save
from django.dispatch import receiver


class BeingsListEvent(models.Model):
    EVENT = (
        ('POST', u'POST'),
        ('DELETE', u'DELETE'),
        ('PATCH', u'PATCH'),
    )
    event = models.CharField(u'State', max_length=10, choices=EVENT)

    class Meta:
        verbose_name = u'Beings list event'
        verbose_name_plural = u'Beings list events'

    def __str__(self):
        return self.event

    def get_event(self):
        if self.event == 'PATCH':
            return 'patch happened'
        return self.event

    def get_absolute_url(self):
        return "/being/%i/" % self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        topic_url = reverse('being-list-event')
        ping_hub('https://%s%s' % (get_current_site(settings.SITE_ID).domain, topic_url))
        super(BeingsListEvent, self).save()


class BeingsEvent(models.Model):
    being = models.ForeignKey(Being, related_name='being_related')
    prev_state = models.CharField(u'Prev state', max_length=10, default='new')

    class Meta:
        verbose_name = u'Being event'
        verbose_name_plural = u'Beings events'

    def __str__(self):
        return self.being.name

    def get_absolute_url(self):
        return "/being/%i/" % self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        topic_url = reverse('beings-event', kwargs={'slug': self.being.slug})
        ping_hub('https://%s%s' % (get_current_site(settings.SITE_ID).domain, topic_url))
        super(BeingsEvent, self).save()


@receiver(post_save, sender=Being)
def send_pubsub_state_mess(sender, instance, update_fields, **kwargs):
    state = instance.state
    query_url = '/state-query/%s' % state
    ping_hub('https://%s%s' % (get_current_site(settings.SITE_ID).domain, query_url))