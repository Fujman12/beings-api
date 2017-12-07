"""main_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from being.views import IndexView, schema_view
from feed_events.feeds import Rss, Atom, AtomList, AtomDetail, AtomQueryParametr

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('api_v0.urls')),
    url(r'^$', IndexView.as_view()),
    url(r'^swagger/$', schema_view),
    url(r'^channels/rss/$', Rss()),
    url(r'^channels/atom/$', Atom()),
    url(r'^channels/atom/list-display/$', AtomList(), name='atom-list'),
    url(r'^channels/atom/detail/(?P<slug>[\-\w]+)/$', AtomDetail(), name='atom-detail'),
    url(r'^channels/atom/query/(?P<state>[\-\w]+)/$', AtomQueryParametr(), name='atom-query_parameter'),
]
