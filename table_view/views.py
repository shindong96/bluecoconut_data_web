from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from .models import *
import matplotlib.pyplot as plt
from .lib import *
from .dataview import *

def get_cycle():
    queryset = ArgoInfo.objects.all().values("Cycle").order_by("Cycle").distinct()
    return queryset

class TableListView(ListView):
    template_name = 'table_view_main.html'

    def get_queryset(self):
        search_num = self.request.GET.get('search-num', None)
        search_open = self.request.GET.get('open-search', None)
        search_work = self.request.GET.get('work-search', None)
        queryset = Argo.objects.filter(active=1).all()
        
        if search_open is not None:
            if int(search_open) == -1:
                pass
            else:
                queryset = queryset.filter(Open_state=search_open)
        
        if search_work is not None:
            if int(search_work) == -1:
                pass
            else:
                queryset = queryset.filter(Live=search_work)

        if search_num is not None and search_num != "":
            queryset = queryset.filter(Serial_number__contains=str(search_num))  # cotains로 하면 포함된 키워드 검색

        plt.switch_backend('Agg')
        #data_print()
        #ts_diagram()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TableListView, self).get_context_data(**kwargs)
        context['page_range'], context['contacts'] = PaginatorManager(self.request, self.get_queryset())
        #context['form'] = ArgoForm()
        return context

class TableDetailListView(ListView):
    template_name = 'table_view_detail.html'
    model = ArgoInfo

    def get_queryset(self):
        cycle = self.request.GET.get('cycleSelect', None)
        queryset = ArgoInfo.objects.filter(argo_id=self.kwargs['pk'])

        if cycle is not None:
            if int(cycle) == -1:
                pass
            else:
                queryset = queryset.filter(Cycle=cycle)
        plt.switch_backend('Agg')
        cycle_csv_create(self.kwargs['pk'], cycle)
        #ts_diagram()
        #data_view_function(self.kwargs['pk'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TableDetailListView, self).get_context_data(**kwargs)
        cycleSelect = self.request.GET.get('cycleSelect', None)
        context['page_range'], context['contacts'] = PaginatorManagerFilter(self.request, self.get_queryset(),cycleSelect)
        #context['form'] = ArgoForm()
        context['CycleLists'] = get_cycle()
        if cycleSelect is not None:
            context['cycleSelect'] = int(cycleSelect)
        else:
            context['cycleSelect'] = cycleSelect

        print(cycleSelect)
        return context