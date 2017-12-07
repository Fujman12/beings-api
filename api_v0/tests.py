# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework.test import APITestCase
from being.models import Being

factory = APIRequestFactory()


class BeingsListTest(APITestCase):
    def setUp(self):

        Being.objects.create(name="test")

    def test_post(self):
        self.request = factory.post('/beings/', {'name': 'Vasya'}, format='json')

    def test_get(self):
        self.request = factory.get('/beings/', format='json')


class BeingsTest(TestCase):

    def test_patch(self):
        self.request = factory.patch('/being/1/', {'state': 'new'}, format='json')

    def test_delete(self):
        self.request = factory.delete('/being/', {'id': '1'}, format='json')