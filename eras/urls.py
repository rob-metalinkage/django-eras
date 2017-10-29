# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^era/~create/$",
        view=views.eraCreateView.as_view(),
        name='era_create',
    ),
    url(
        regex="^era/(?P<pk>\d+)/~delete/$",
        view=views.eraDeleteView.as_view(),
        name='era_delete',
    ),
    url(
        regex="^era/(?P<pk>\d+)/$",
        view=views.eraDetailView.as_view(),
        name='era_detail',
    ),
    url(
        regex="^era/(?P<pk>\d+)/~update/$",
        view=views.eraUpdateView.as_view(),
        name='era_update',
    ),
    url(
        regex="^era/$",
        view=views.eraListView.as_view(),
        name='era_list',
    ),
	]
