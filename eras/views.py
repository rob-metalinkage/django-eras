# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Era,
)


class eraCreateView(CreateView):

    model = Era


class eraDeleteView(DeleteView):

    model = Era


class eraDetailView(DetailView):

    model = Era


class eraUpdateView(UpdateView):

    model = Era


class eraListView(ListView):

    model = Era

class eraIntervals(ListView):

    model = EraScheme

class eraTimeline(ListView):
    """Generate a d3 interactive timeline vizualisation
    
    Hierarchical D3 viz, with zoom and link to details. Todo. Todo later still... make link configurable
    """
    model = EraScheme
