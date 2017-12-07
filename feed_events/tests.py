try:
    from unittest import mock
except ImportError:
    import mock

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from django_push import UA
from django_push.publisher import ping_hub


class PubTestCase(TestCase):
    @mock.patch('requests.post')
    @override_settings(PUSH_HUB='http://hub.example.com')
    def test_ping_settings(self, post):
        post.return_value = 'Response'
        ping_hub('http://example.com/feed')
        post.assert_called_once_with(
            'http://hub.example.com',
            headers={'User-Agent': UA},
            data={'hub.url': 'http://example.com/feed',
                  'hub.mode': 'publish'})

    @mock.patch('requests.post')
    @override_settings(PUSH_HUB='https://pubsubhubbub.appspot.com')
    def test_ping_settings_override(self, post):
        post.return_value = 'Response'
        ping_hub('http://example.com/feed', hub_url='http://google.com')
        post.assert_called_once_with(
            'http://google.com',
            headers={'User-Agent': UA},
            data={'hub.url': 'http://example.com/feed',
                  'hub.mode': 'publish'})

    def test_no_hub(self):
        response = self.client.get(reverse('atom-list'))
        self.assertEqual(response.status_code, 200)