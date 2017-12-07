from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api_v0.views import BeingList, BeingDetail, BeingEventApiView, BeingsListEventApiView, BeingEventQueryApiView

urlpatterns = [
    url(r'^beings/?(?P<state>(.*))/?$', BeingList.as_view(), name="being-list"),
    url(r'^being/(?P<slug>[\-\w]+)/$', BeingDetail.as_view(), name="being-detail"),
    url(r'^being-event/(?P<slug>[\-\w]+)/$', BeingEventApiView.as_view(), name="beings-event"),
    url(r'^being-list-event/$', BeingsListEventApiView.as_view(), name="being-list-event"),
    url(r'^state-query/?(?P<state>(.*))/?$', BeingEventQueryApiView.as_view(), name="state-query"),
]
urlpatterns = format_suffix_patterns(urlpatterns)