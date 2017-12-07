# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from being.models import Being
from feed_events.models import BeingsEvent, BeingsListEvent
from api_v0.serializers import BeingListSerializer, BeingDetailSerializer, BeingEventSerializer,\
    BeingsListEventSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.schemas import AutoSchema
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import coreapi
import coreschema


class BeingList(ListCreateAPIView):
    queryset = Being.objects.all()
    serializer_class = BeingListSerializer
    lookup_field = 'slug'

    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "state",
            required=False,
            location="path",
            schema=coreschema.String()
        ),
    ])

    def get_queryset(self):
        queryset = Being.objects.all()

        state = self.kwargs['state'].rstrip('/')
        if state == '{state}':
            state = False
        if state:
            queryset = Being.objects.filter(state=state)
            return queryset
        return queryset

    def post(self, request, *args, **kwargs):
        bel = BeingsListEvent(event='POST')
        bel.save()
        return self.create(request, *args, **kwargs)

    def finalize_response(self, request, *args, **kwargs):
        response = super(BeingList, self).finalize_response(request, *args, **kwargs)
        topic_url = reverse('being-list-event')
        state = kwargs['state'].rstrip('/')
        if state == '{state}':
            state = False
        if state:
            topic_url = '/state-query/%s' % state
        full_url = ('https://%s%s' % (get_current_site(settings.SITE_ID).domain, topic_url))
        response['Link'] = '<' + full_url + '>; rel="self, <' + settings.PUSH_HUB + '>; rel="hub"'
        return response


class BeingDetail(RetrieveUpdateDestroyAPIView):
    queryset = Being.objects.all()
    serializer_class = BeingDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug'].lower()
        obj = get_object_or_404(Being, slug=slug)
        return obj

    def delete(self, request, *args, **kwargs):
        bel = BeingsListEvent(event='DELETE')
        bel.save()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        bel = BeingsListEvent(event='PATCH')
        bel.save()
        being = get_object_or_404(Being, slug=kwargs['slug'])
        prev_state = being.state
        be = BeingsEvent(being=being, prev_state=prev_state)
        be.save()
        return self.update(request, *args, **kwargs)

    def finalize_response(self, request, *args, **kwargs):
        response = super(BeingDetail, self).finalize_response(request, *args, **kwargs)
        slug = kwargs['slug'].lower()
        rss_url = reverse('beings-event', kwargs={'slug': slug})
        full_url = ('https://%s%s' % (get_current_site(settings.SITE_ID).domain, rss_url))
        response['Link'] = '<' + settings.PUSH_HUB + '>; rel="hub", <' + full_url + '>; rel="self"'
        return response


class BeingsListEventApiView(ListAPIView):
    queryset = BeingsListEvent.objects.order_by('-id')
    serializer_class = BeingsListEventSerializer


class BeingEventApiView(ListAPIView):
    serializer_class = BeingEventSerializer

    def get_queryset(self):
        queryset = BeingsEvent.objects.order_by('-id')
        slug = self.kwargs['slug'].lower()
        obj = get_object_or_404(Being, slug=slug)
        queryset = queryset.filter(being=obj)
        return queryset


class BeingEventQueryApiView(ListAPIView):
    serializer_class = BeingEventSerializer

    @property
    def get_state(self):
        state = self.kwargs['state'].rstrip('/')
        if state or not state == '{state}':
            return state
        return False

    def get_queryset(self):
        if self.get_state:
            return BeingsEvent.objects.filter(being__state=self.get_state).order_by('-id')
        return BeingsEvent.objects.all().order_by('-id')


