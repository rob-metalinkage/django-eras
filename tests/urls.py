# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from eras.urls import urlpatterns as eras_urls

urlpatterns = [
    url(r'^', include(eras_urls, namespace='eras')),
]
