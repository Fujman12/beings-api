import requests

from django.conf import settings


def ping_hub(topic_url, hub_url=None):
    """
    Makes a POST request to the hub. If no hub_url is provided, the
    value is fetched from the PUSH_HUB setting.
    Returns a `requests.models.Response` object.
    """
    if hub_url is None:
        hub_url = getattr(settings, 'PUSH_HUB', None)
    if hub_url is None:
        raise ValueError("Specify hub_url or set the PUSH_HUB setting.")
    headers = {
        'Link': '<' + topic_url + '>; rel="self", <' + hub_url + '>; rel="hub"'
    }
    params = {
        'hub.mode': 'publish',
        'hub.topic': topic_url,
        # 'hub.url': topic_url,
    }
    return requests.post(hub_url, data=params, headers=headers)