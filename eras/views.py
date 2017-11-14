# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from django.http import HttpResponse
import json

from .models import (
    Era,EraScheme
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

def eraIntervals(request,scheme_id):
    if request.GET.get('pdb') :
        import pdb; pdb.set_trace()
    try:
        start = int(request.GET.get('start'))
    except:
        start = None
    try:
        end = int(request.GET.get('end'))
    except:
        end = None        
    scheme = EraScheme.objects.get(id=scheme_id)
    return HttpResponse(    scheme.json_intervals(start=start,end=end),  content_type="application/json")
   

def eraTimeline(request,scheme_id):
    """Generate a d3 interactive timeline vizualisation
    
    Hierarchical D3 viz, with zoom and link to details. Todo. Todo later still... make link configurable
    """
    model = EraScheme
